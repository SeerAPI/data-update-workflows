from typing_extensions import NotRequired, TypedDict

UNITY_ASSETS_REPO = "SeerAPI/seer-unity-assets"
PET_ANIM_REPO = "SeerAPI/seer-unity-assets-pet_anim_part"


class PackageConfig(TypedDict):
    updater_name: str
    extractor_name: str
    update_args: list[str]
    skip_extract: bool
    min_size: NotRequired[str | int]
    max_size: NotRequired[str | int]
    target_repo: NotRequired[str]
    push_patterns: NotRequired[list[str]]


CONFIG: dict[str, PackageConfig] = {
    "ConfigPackage": {
        "updater_name": "newseer.config",
        "extractor_name": "newseer",
        "update_args": [],
        "skip_extract": False,
    },
    "DefaultPackage": {
        "updater_name": "newseer.default",
        "extractor_name": "newseer",
        "update_args": [
            "*game_audios_cv*",
            "*art_ui_pettype*",
            "*art_ui_battleeffect*",
            "*art_ui_avatar*",
            "*art_ui_titlebg*",
            "*art_ui_namecard*",
            "*art_ui_common*",
            "*art_ui_effecticon*",
            "*assets_art_ui_assets_pet_head*",
            "*assets_art_ui_assets_pet_body*",
            "*assets_art_ui_assets_archive*",
            "*assets_art_ui_assets_countermark*",
            "*assets_art_ui_assets_item*",
            "*art_ui_achieve*",
            "*art_ui_assets_achieve_icon*",
            "*art_ui_item_cloth_prev*",
            "*art_ui_expression*",
            "*art_ui_fitment*",
            "*art_ui_nono*",
            "*art_ui_item_*",
            "*art_ui_soulbead*",
            "*art_ui_countermark_*",
            "*art_ui_achieve*",
            "*art_autocard_texture_cards*",
            "*art_autocard_texture_roles*",
            "*art_autocard_texture_minipet*",
        ],
        "skip_extract": False,
    },
    "PetAnimPackage": {
        "updater_name": "newseer.pet",
        "extractor_name": "newseer",
        "update_args": [],
        "min_size": "5M",
        "skip_extract": True,
        "target_repo": PET_ANIM_REPO,
        "push_patterns": ["newseer/", "package-manifests/"],
    },
}
