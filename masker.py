#!/usr/bin/env python
# -*- coding: utf-8 -*

import os
import time
import argparse
from operator import itemgetter


def readable_dir(prospective_dir):
    if not os.path.isdir(prospective_dir):
        raise argparse.ArgumentTypeError("readable_dir:{0} is not a valid path".format(prospective_dir))
    if os.access(prospective_dir, os.R_OK):
        return prospective_dir
    else:
        raise argparse.ArgumentTypeError("readable_dir:{0} is not a readable dir".format(prospective_dir))


def process_annotations(entities):
    keys = set()
    entities = [keys.add(sublist[0]) or sublist for sublist in entities if sublist[0] not in keys]
    entities = [keys.add(sublist[1]) or sublist for sublist in entities if sublist[1] not in keys]
    previous_end = 0
    for entry in sorted(entities, key=itemgetter(0)):  # Sort annotation by starting offset
        start = entry[0]
        end = entry[1]
        form = entry[3]
        if entry[0] < previous_end:
            if not args.quiet:
                print("\tWARNING! " + form + "(" + str(start) + "," + str(end)
                      + ") overlaps with a previous annotation.")
            entities.remove(entry)
        previous_end = end
    return entities


def load_custom_masks():
    if args.custom_file:
        try:
            custom_masks = {}
            for row in args.custom_file.readlines():
                line = row.strip()
                label = line.split("\t")[0]
                mask = line.split("\t")[1]
                custom_masks[label] = mask
        except IOError:
            if not args.quiet:
                print("File " + args.custom_file + " does not exist!")
    return custom_masks


def load_annotations(ann_file):
    annotations = []
    # Check if custom mask labels option is activated; if true load them
    if args.custom_file:
        custom_masks = load_custom_masks()
    for row in ann_file:
        line = row.strip()
        if line.startswith("T"):  # Lines is a Brat TAG
            try:
                label = line.split("\t")[1].split()
                tag = label[0]
                start = int(label[1])
                end = int(label[2])
                form = line.split("\t")[2]
            except IndexError:
                print("ERROR! Index error while splitting sentence '" + line + "' in document '" + ann_file + "'!")
            # If custom_only option is activated store only labels on custom_file
            if args.custom_only:
                if tag in custom_masks.keys():
                    tag = custom_masks[tag]
                    annotations.append([start, end, tag, form])
            else:
                # If custom_file option is activated, replace tag for custom tag in the custom masks file
                if args.custom_file:
                    if tag in custom_masks.keys():
                        tag = custom_masks[tag]
                annotations.append([start, end, tag, form])
        else:  # Line is a Brat comment
            if args.verbose:
                print("\tSkipping line (comment):\t" + line)
    # Remove duplicated and overlapping annotations and sort
    annotations = process_annotations(annotations)
    return annotations


def process_file(text_full_filename, tagged_full_filename):
    try:
        text_file = open(text_full_filename, "r")
        text_data = text_file.read()
        text_file.close()
    except IOError:
        if not args.quiet:
            print("File " + text_file + " does not exist!")
    try:
        tagged_file = open(tagged_full_filename, "r")
        # Read Brat annotation file
        annotations = load_annotations(tagged_file)
        # The size of the form and the tag may be of different lengths
        offset = 0  # Offset to update start and end offsets in top-down masking (comment if using bottom-up masking)
        for entry in sorted(annotations, key=itemgetter(0)):
            start = entry[0] + offset  # Remove '+ offset' if using bottom-up masking)
            end = entry[1] + offset  # Remove '+ offset' if using bottom-up masking)
            tag = entry[2]
            form = entry[3]
            text_data = text_data[:start] + tag + text_data[end:]  # Mask text
            offset = offset + len(tag) - len(form)  # Update offset (comment if using bottom-up masking)
        tagged_file.close()
    except IOError:
        if not args.quiet:
            print("File " + tagged_file + " does not exist!")
    return text_data


def process_corpus(corpus_list, input_dir, tagged_dir, output_dir):
    if not args.quiet:
        print ("Processing corpus...")
    for filename in corpus_list:
        text_full_filename = os.path.join(input_dir, filename) + ".txt"
        tagged_full_filename = os.path.join(tagged_dir, filename) + ".ann"
        output_full_filename = os.path.join(output_dir, filename) + ".txt"
        masked_text = process_file(text_full_filename, tagged_full_filename)
        output_file = open(output_full_filename, "w")
        output_file.write(masked_text)
    if not args.quiet:
        print("\nCorpus processing completed!\n")


def load_corpus(input_dir, tagged_dir):
    if not args.quiet:
        print ("Loading list of files...")
    corpus = []
    for subdir, dirs, files in os.walk(input_dir):
        for text_filename in files:
            if text_filename.endswith(".txt"):
                tagged_filename = os.path.splitext(text_filename)[0] + ".ann"
                tagged_full_filename = os.path.join(tagged_dir, tagged_filename)
                if os.path.isfile(tagged_full_filename):
                    corpus.append(os.path.splitext(text_filename)[0])
                else:
                    if not args.quiet:
                        print ("\tFile " + tagged_full_filename + " does not exist!")
    if not args.quiet:
        print ("Corpus file list loaded!\n")
    return corpus


if __name__ == '__main__':

    start_time = time.time()
    # Read command line parameters
    parser = argparse.ArgumentParser(description="Script to mask a corpus using Brat annotations.")
    parser.add_argument("-i", "--input_dir",
                        type=readable_dir,
                        help="Folder with the original input files",
                        default='input')
    parser.add_argument("-t", "--tagged_dir",
                        type=readable_dir,
                        help="Folder with Brat annotation files",
                        default='tagged')
    parser.add_argument("-o", "--output_dir",
                        type=readable_dir,
                        help="Folder to store the output masked files",
                        default='output')
    parser.add_argument("-c", "--custom_file",
                        type=argparse.FileType('r'),
                        help="Path to file with custom masks for annotations")
    parser.add_argument("-co", "--custom-only",
                       help="Use only labels in custom masks file",
                       action="store_true")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose",
                       help="Increase output verbosity",
                       action="store_true")
    group.add_argument("-q", "--quiet",
                       help="Do not print anything",
                       action="store_true")
    args = parser.parse_args()
    if args.custom_only and args.custom_file is None:
        parser.error("--custom_only option requires --custom_file option.")
    # Load files and process corpus
    if not args.quiet:
        print("Masking your corpus...\n")
    my_corpus_list = load_corpus(args.input_dir, args.tagged_dir)
    process_corpus(my_corpus_list, args.input_dir, args.tagged_dir, args.output_dir)
    if not args.quiet:
        print("Processing time: %.2f seconds.\n" % (time.time() - start_time))
