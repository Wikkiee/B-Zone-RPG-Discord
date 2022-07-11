
#----------------> SFPD test server- Starts here <-----------

# sfpd_roles = {
#     "rank_0":990546436246626334,
#     "rank_1":990545175036190771,
#     "rank_2":990545360227278898,
#     "rank_3":990545423540314112,
#     "rank_4":990545487461486692,
#     "rank_5":990545653576892426,
#     "rank_6":990485264096956416,
#     "rank_leader":990545771768217621,
#     "unverified":990546521156091945,
#     "verified":990547306694713394,
#     "ex_member":990546639087366174,
#     "other_faction_members":991025432843411506,
#     "everyone":859471645235085382
# }

#----------------> SFPD test server- ends here <-----------


#----------------> SFPD main server- Starts here <-----------

sfpd_roles = {
    "rank_0":995215424893489245,
    "rank_1":993901020130320485,
    "rank_2":993901307205259354,
    "rank_3":993901349144104990,
    "rank_4":993901382832758875,
    "rank_5":993901426864570479,
    "rank_6":993901466425233479,
    "rank_leader":993901502026489998,
    "unverified":995215649129373736,
    "verified":995215577234800674,
    "ex_member":993902467983097938,
    "other_faction_members":995214555594625044,       
    "everyone":859471645235085382
}

#----------------> SFPD main server- Starts ends here <-----------

def get_rank_role(faction,rank):
    if(faction == "SFPD"):
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
        
    # if(faction == "SF School Instructors"):
    #     if(rank == "Candidate (0)"):
    #         return sfsi_roles["rank_0"]
    #     elif(rank == "SF Trainee (1)"):
    #         return sfsi_roles["rank_1"]
    #     elif(rank == "SF Instructor (2)"):
    #         return sfsi_roles["rank_2"]
    #     elif(rank == "SF Senior Instructor (3)"):
    #         return sfsi_roles["rank_3"]
    #     elif(rank == "SF Supervisor (4)"):
    #         return sfsi_roles["rank_4"]
    #     elif(rank == "SF Manager (5)"):
    #         return sfsi_roles["rank_5"]
    #     elif(rank == "SF Under Boss (6)"):
    #         return sfsi_roles["rank_6"]
    #     elif(rank == "SF Boss (Leader)"):
    #         return sfsi_roles["rank_leader"]