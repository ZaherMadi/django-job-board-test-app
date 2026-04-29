#!/usr/bin/env python
"""
Script d'initialisation Azure Blob Storage.

Au démarrage du conteneur :
  1. Crée les conteneurs `static` et `media` (s'ils n'existent pas)
     avec un accès public au niveau blob (les CSS doivent être lisibles
     directement par le navigateur).
  2. Upload le contenu des dossiers `staticfiles/` et `media/` dans
     leurs conteneurs respectifs en renseignant le bon Content-Type
     (sinon le navigateur n'interprète pas les CSS comme des feuilles
     de style).
"""

import mimetypes
import os
import sys
from pathlib import Path

from azure.core.exceptions import ResourceExistsError
from azure.storage.blob import BlobServiceClient, ContentSettings


def _guess_content_type(file_path: Path) -> str:
    """Devine le content-type d'un fichier en se basant sur son extension."""
    content_type, _ = mimetypes.guess_type(file_path.name)
    return content_type or "application/octet-stream"


def initialize_azure_storage() -> bool:
    storage_account_name = os.environ.get("STORAGE_ACCOUNT_NAME")
    storage_account_key = os.environ.get("STORAGE_ACCOUNT_KEY")

    if not storage_account_name or not storage_account_key:
        print("ℹ️  Variables STORAGE_ACCOUNT_NAME / STORAGE_ACCOUNT_KEY absentes : on saute l'upload Azure.")
        return True

    try:
        connection_string = (
            f"DefaultEndpointsProtocol=https;"
            f"AccountName={storage_account_name};"
            f"AccountKey={storage_account_key};"
            f"EndpointSuffix=core.windows.net"
        )
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Les deux conteneurs sont publics au niveau "blob" pour que le
        # navigateur puisse lire les CSS / images sans token.
        containers = [
            {"name": "static", "public_access": "blob"},
            {"name": "media", "public_access": "blob"},
        ]

        print("\n📦 Création des conteneurs...")
        for cfg in containers:
            try:
                blob_service_client.create_container(
                    name=cfg["name"],
                    public_access=cfg["public_access"],
                )
                print(f"✅ Conteneur '{cfg['name']}' créé (public_access={cfg['public_access']})")
            except ResourceExistsError:
                print(f"ℹ️  Conteneur '{cfg['name']}' existe déjà")
            except Exception as exc:
                print(f"❌ Erreur création conteneur '{cfg['name']}': {exc}")
                return False

        uploads = [
            {
                "local_path": Path("staticfiles"),
                "container_name": "static",
                "description": "Fichiers Statiques (CSS, JS)",
            },
            {
                "local_path": Path("media"),
                "container_name": "media",
                "description": "Fichiers Media (uploads utilisateurs)",
            },
        ]

        print("\n📤 Upload des fichiers...")
        for migration in uploads:
            local_path: Path = migration["local_path"]
            container_name: str = migration["container_name"]
            description: str = migration["description"]

            if not local_path.exists():
                print(f"ℹ️  {description} : dossier '{local_path}' absent, on passe.")
                continue

            print(f"\n📁 {description} → conteneur '{container_name}'")
            container_client = blob_service_client.get_container_client(container_name)

            files = [f for f in local_path.rglob("*") if f.is_file()]
            if not files:
                print("   (aucun fichier)")
                continue

            uploaded = 0
            for file_path in files:
                relative_path = file_path.relative_to(local_path)
                blob_name = str(relative_path).replace("\\", "/")
                content_type = _guess_content_type(file_path)

                try:
                    with open(file_path, "rb") as data:
                        container_client.upload_blob(
                            name=blob_name,
                            data=data,
                            overwrite=True,
                            content_settings=ContentSettings(content_type=content_type),
                        )
                    print(f"   ✅ {blob_name}  [{content_type}]")
                    uploaded += 1
                except Exception as exc:
                    print(f"   ⚠️  Erreur upload {blob_name}: {exc}")

            print(f"   → {uploaded}/{len(files)} fichier(s) uploadé(s)")

        print("\n✅ Initialisation Azure Blob Storage terminée")
        return True

    except Exception as exc:
        print(f"❌ Erreur Azure : {exc}")
        return False


if __name__ == "__main__":
    sys.exit(0 if initialize_azure_storage() else 1)
