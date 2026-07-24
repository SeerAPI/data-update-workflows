import asyncio
import sys

import albi0

from scripts._common import (
    DataRepoManager,
    get_current_time_str,
    write_to_github_output,
)
from scripts.seer_unity_assets.config import CONFIG, PackageConfig


def get_manifest_path(package_name: str) -> str:
    return f"package-manifests/{package_name}.json"


def get_bundle_path(package_name: str) -> str:
    return f"newseer/assetbundles/{package_name}/*"


async def process_package(
    *,
    package_name: str,
    config: PackageConfig,
    force: bool = False,
):
    async with albi0.session():
        await albi0.update_resources(
            config["updater_name"],
            *config["update_args"],
            manifest_path=get_manifest_path(package_name),
            timeout=180.0,
            ignore_version=force,
            min_size=config.get("min_size"),
            max_size=config.get("max_size"),
        )
        if not config.get("skip_extract"):
            await albi0.extract_assets(
                config["extractor_name"],
                get_bundle_path(package_name),
                max_workers=2,
            )


def parse_args() -> tuple[bool, str, set[str] | None]:
    force = "--force" in sys.argv
    repo_path = "."
    packages: set[str] | None = None

    if "--repo-path" in sys.argv:
        repo_path = sys.argv[sys.argv.index("--repo-path") + 1]

    if "--packages" in sys.argv:
        packages = {
            name.strip()
            for name in sys.argv[sys.argv.index("--packages") + 1].split(",")
            if name.strip()
        }

    return force, repo_path, packages


def get_push_patterns(package_name: str, config: PackageConfig) -> list[str]:
    if push_patterns := config.get("push_patterns"):
        return push_patterns

    files_fp = (
        f"{config['extractor_name']}/assets/"
        if config.get("extractor_name") and not config.get("skip_extract")
        else get_bundle_path(package_name)
    )
    return ["package-manifests/", files_fp]


async def run(
    *,
    force: bool = False,
    repo_path: str = ".",
    packages: set[str] | None = None,
):
    albi0.load_all_plugins()

    manager = DataRepoManager.from_checkout(repo_path)
    has_update = False

    for package_name, config in CONFIG.items():
        if packages is not None and package_name not in packages:
            continue

        remote_version = await albi0.get_remote_version(config["updater_name"])
        print(f"⚙️ 正在更新资源包 {package_name}...")
        await process_package(
            package_name=package_name,
            config=config,
            force=force,
        )
        print(f"✅ 资源包 {package_name} 更新完成")
        if manager.commit_and_push(
            f"{package_name}: Update to {remote_version} | Time: {get_current_time_str()}",
            files=get_push_patterns(package_name, config),
        ):
            has_update = True

    if has_update:
        write_to_github_output("has_update", "true")


def main():
    force, repo_path, packages = parse_args()
    asyncio.run(run(force=force, repo_path=repo_path, packages=packages))
