import sys
import gzip
import argparse
import re
import logging

def error_exit(message):
    logging.error(message)
    sys.exit()


def open_file(file_name, mode="r"):
    access_type = mode
    if sys.version_info >= (3,): access_type = mode + "t"
    if file_name.endswith("gz"):
        return gzip.open(file_name, access_type)
    else:
        return open(file_name, access_type)


def read_recursively(sequence, bp, ix):

    structure = []
    while ix < len(bp):

        label1 = sequence[ix]
        if args.positions:
            label1 = "{}{}".format(sequence[ix], ix+1)
        if bp[ix] == '.':
            structure.append(label1)
        elif bp[ix] == '(':
            [ix, structure_in] = read_recursively(sequence, bp, ix+1)
            label2 = sequence[ix]
            if args.positions:
                label2 = "{}{}".format(sequence[ix], ix + 1)
            structure.append([label1 + " - " + label2, structure_in])
        else:
            return [ix, structure]
        ix += 1

    return structure


def read_structure(f):
    lines = f.readlines()

    ix_sequence = 0
    if lines[0].startswith(">"):
        ix_sequence = 1

    ix_ss = 0
    for ix in range(ix_sequence,len(lines)):
        if re.search(r'[,\(\)]', lines[ix]):
            ix_ss = ix
            break

    if ix_ss == 0:
        error_exit("Secondary structure in the dot-bracket notation not found.")

    sequence = re.sub(r'\s+', '', ''.join(lines[ix_sequence:ix_ss]))
    dp = re.sub(r'\s+', '', ''.join(lines[ix_ss:]))

    if len(sequence) != len(dp):
        error_exit("Length of the sequence and secondary strucutres do not match.")

    return read_recursively(sequence, dp, 0)


def write_recursively(s, f, id_parent="n", prefix=""):
    seq = 0
    level_ids = []
    for node in s:
        seq += 1
        id_node = id_parent + "_" + str(seq)
        level_ids.append(id_node)
        if type(node) is list:
            style = "label=\"{}\" shape=rectangle style=rounded".format(node[0])
        else:
            style = "label=\"{}\"".format(node)
        f.write('{}{}[{}]\n'.format(prefix, id_node, style))
        if type(node) is list:
            write_recursively(node[1], f, id_node, prefix + "  ")

    if id_parent != "n":
        for id_node in level_ids:
            f.write("{}{} -- {}\n".format(prefix, id_parent, id_node))

    if len(level_ids) > 1:
        f.write("{}{{rank=same;{} }}\n".format(prefix, " ".join(level_ids)))


def write_structure(s, f):
    f.write('graph{ node[penwidth=3 fontsize=24] edge[penwidth=3]\n ')
    write_recursively(s, f)
    f.write("}\n")


def main():
    with open_file(args.input, "r") as fr:
        s = read_structure(fr)
        with (sys.stdout if args.output is None else open_file(args.output, "w")) as fw:
            write_structure(s, fw)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input",
                        required=True,
                        metavar='FILE',
                        help="Input structure in Vienna format.")
    parser.add_argument("-o", "--output",
                        metavar='FILE',
                        help="Output file name for the dot file. "
                             "If non entered, the graph will be writen to the standard output.")
    parser.add_argument("-p", "--positions",
                        action='store_true',
                        help="Includes positions of nucleotides in node labels when turned on.")

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] %(module)s - %(message)s',
        datefmt='%H:%M:%S')

    main()