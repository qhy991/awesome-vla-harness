"""Inspect a LeRobot dataset without any robot hardware attached.

Run with:

    python examples/lerobot-dataset/inspect_dataset.py
"""

from lerobot.datasets.lerobot_dataset import LeRobotDataset


def main() -> None:
    dataset = LeRobotDataset("lerobot/aloha_mobile_cabinet")

    print(f"num_frames={len(dataset)}")

    sample = dataset[0]

    print("keys:")
    for key in sorted(sample.keys()):
        print(f"  - {key}")

    if "action" in sample:
        print("action shape:", sample["action"].shape)


if __name__ == "__main__":
    main()
