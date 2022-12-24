#!/usr/bin/env python3

# importing required libraries
import csv
import argparse
import random
import sys

# main function
def main(file, members_per_group=4, reassign=False):
    # reading csv file
    with open(file, "r") as f:
        reader = csv.reader(f)
        names_list = list(reader)

    # putting all the names in one list
    all_names = []
    for element in names_list:
        all_names.append(element[0])

    # splitting groups
    all_groups = {}
    group_num = 0
    while len(all_names) > 0:
        group = []
        for i in range(min(members_per_group, len(all_names))):
            group.append(all_names.pop(random.randrange(0, len(all_names))))

        # if reassign is set to true, reassign members of the incomplete group to the rest of the groups
        if reassign and len(group) < members_per_group:
            while len(group) > 0:
                random_group = random.randrange(1, len(all_groups))
                while len(all_groups[f"Group {random_group}"]) > members_per_group:
                    random_group = random.randrange(1, len(all_groups))

                all_groups[f"Group {random_group}"].append(group.pop())

        # if it's not the last group then add another group
        else:
            group_num += 1
            all_groups[f"Group {group_num}"] = group

    # writing results in a csv file
    with open("./groups.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(all_groups.items())


if __name__ == "__main__":
    # parse command line arguments
    parser = argparse.ArgumentParser(
        description=main.__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-m", "--members_per_group", help="number of members per group", type=int
    )
    parser.add_argument(
        "-r",
        "--reassign",
        help="reassign members of the last incomplete group to the rest of the groups",
        action="store_true",
    )
    parser.add_argument("FILE", help="csv file with member names on separate lines")
    args = parser.parse_args()

    # get arguments and set defaults
    members_per_group = (
        args.members_per_group if args.members_per_group is not None else 4
    )
    reassign = args.reassign if args.reassign is not None else False

    # call main function
    main(args.FILE, members_per_group, reassign)

    # print done message and exit
    print("Done")
    sys.exit(0)
