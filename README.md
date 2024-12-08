# mmtools

This is a helper package for mm family projects. It searches for types of mm projects and prints out their locations and import statements.

Usage example:

```bash
mmfind CocoDataset
```

Output:

```
/home/user/2024/references/mmdetection-2.28.2/mmdet/datasets/coco_occluded.py:16
        class OccludedSeparatedCocoDataset(CocoDataset):
        >> from mmdet.datasets.coco_occluded import OccludedSeparatedCocoDataset

/home/user/2024/references/mmdetection-2.28.2/mmdet/datasets/coco.py:23
        class CocoDataset(CustomDataset):
        >> from mmdet.datasets.coco import CocoDataset
```

By default, the tool tries to search for the type in all installed mm family projects. If you want to search for a specific path, you can add it to the `~/.config/mmtools/mm_packages.json` file (create the file if it doesn't exist). For example, to search for `stream_petr` project, you can add the following entry to `mm_packages.json`:

```json
[
    {
        "name": "stream_petr",
        "location": "/home/user/2024/StreamPETR/projects",
    }
]
```

## Installation

```bash
git clone https://github.com/hyuyao/mmtools.git
cd mmtools
pip install -e .
```

## Note

This project has been set up using PyScaffold 4.6. For details and usage
information on PyScaffold see https://pyscaffold.org/.
