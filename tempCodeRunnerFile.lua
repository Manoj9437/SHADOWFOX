
league_members = [
    "Superman",
    "Batman",
    "Wonder Woman",
    "Flash",
    "Aquaman",
    "Green Lantern"
]
print(f"Phase 1 - League gathers: {league_members}")
print(f"Phase 1 - Total heroes present: {len(league_members)}")

additional_heroes = ["Batgirl", "Nightwing"]
league_members.extend(additional_heroes)
print(f"Phase 2 - Reinforcements arrive: {league_members}")

league_members.remove("Wonder Woman")
league_members.insert(0, "Wonder Woman")
print(f"Phase 3 - Wonder Woman takes command: {league_members}")

index_flash = league_members.index("Flash")
index_aquaman = league_members.index("Aquaman")

if index_aquaman < index_flash:
    index_flash, index_aquaman = index_aquaman, index_flash

league_members.remove("Superman")
league_members.insert(index_flash + 1, "Superman")
print(f"Phase 4 - Green Lantern stands between Flash and Aquaman: {league_members}")

league_members = [
    "Cyborg",
    "Shazam",
    "Hawkgirl",
    "Martian Manhunter",
    "Green Arrow"
]
print(f"Phase 5 - A fresh lineup takes shape: {league_members}")

league_members.sort()
print(f"Phase 6 - Sorted roster: {league_members}")
print(f"Phase 6 - Leading the charge: {league_members[0]}")