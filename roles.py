sfsi_roles = {
    "rank_0":991655145647636535,
    "rank_1":991655145647636536,
    "rank_2":991655145647636537,
    "rank_3":991655145647636538,
    "rank_4":991655145647636539,
    "rank_5":991655145668612096,
    "rank_6":991655145668612097,
    "rank_leader":991655145668612098,
    "unverified":991655145647636531,
    "verified":991655145647636532,
    "ex_member":991655145647636534,
    "other_faction_members":991655145647636533
}
sfpd_roles = {
    "rank_0":990546436246626334,
    "rank_1":990545175036190771,
    "rank_2":990545360227278898,
    "rank_3":990545423540314112,
    "rank_4":990545487461486692,
    "rank_5":990545653576892426,
    "rank_6":990485264096956416,
    "rank_leader":990545771768217621,
    "unverified":990546521156091945,
    "verified":990547306694713394,
    "ex_member":990546639087366174,
    "other_faction_members":991025432843411506
}

def get_rank_role(faction,rank):
    if(faction == "SF School Instructors"):
        if(rank == "Candidate (0)"):
            return sfsi_roles["rank_0"]
        elif(rank == "SF Trainee (1)"):
            return sfsi_roles["rank_1"]
        elif(rank == "SF Instructor (2)"):
            return sfsi_roles["rank_2"]
        elif(rank == "SF Senior Instructor (3)"):
            return sfsi_roles["rank_3"]
        elif(rank == "SF Supervisor (4)"):
            return sfsi_roles["rank_4"]
        elif(rank == "SF Manager (5)"):
            return sfsi_roles["rank_5"]
        elif(rank == "SF Under Boss (6)"):
            return sfsi_roles["rank_6"]
        elif(rank == "SF Boss (Leader)"):
            return sfsi_roles["rank_leader"]
    elif(faction == "SFPD"):
        if(rank == "Candidate (0)"):
            return sfpd_roles["rank_0"]
        elif(rank == "Officer (1)"):
            return sfpd_roles["rank_1"]
        elif(rank == "Detective (2)"):
            return sfpd_roles["rank_2"]
        elif(rank == "Sergeant (3)"):
            return sfpd_roles["rank_3"]
        elif(rank == "Lieutenant (4)"):
            return sfpd_roles["rank_4"]
        elif(rank == "Captain (5)"):
            return sfpd_roles["rank_5"]
        elif(rank == "Assistant Chief (6)"):
            return sfpd_roles["rank_6"]
        elif(rank == "Chief (Leader)"):
            return sfpd_roles["rank_leader"]
        