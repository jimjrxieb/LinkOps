import os, json


def save_orb(agent, orb):
    os.makedirs(f"storage/orbs/{agent}", exist_ok=True)
    with open(f"storage/orbs/{agent}/{orb['id']}.json", "w") as f:
        json.dump(orb, f, indent=2)


def save_rune(agent, rune):
    os.makedirs(f"storage/runes/{agent}", exist_ok=True)
    with open(f"storage/runes/{agent}/{rune['id']}.json", "w") as f:
        json.dump(rune, f, indent=2)


def save_approval_if_needed(agent, orb, rune):
    os.makedirs(f"storage/approvals/{agent}", exist_ok=True)
    fname = f"storage/approvals/{agent}/{orb['id']}.json"
    with open(fname, "w") as f:
        json.dump({"orb": orb, "rune": rune}, f, indent=2)


def get_pending_approvals():
    approvals = []
    for agent_dir in os.listdir("storage/approvals"):
        agent_path = f"storage/approvals/{agent_dir}"
        if os.path.isdir(agent_path):
            for fname in os.listdir(agent_path):
                with open(f"{agent_path}/{fname}") as f:
                    approvals.append(json.load(f))
    return approvals


def get_training_digest():
    # TODO: Implement digest generation
    return {
        "processed_today": len(os.listdir("data_lake/sanitized_inputs/")),
        "pending_approvals": len(get_pending_approvals()),
        "agents_updated": ["katie", "igris", "whis"],
    }
