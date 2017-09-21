# -*- encoding: utf-8 -*-
import os
import xml.etree.ElementTree as et
import argparse
import codecs

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-p", action='store', type=str, dest='pathToXml',
                        help="Specify the path to the xml file.")
arg_parser.add_argument("-f", action='store', type=str, dest='pathToSave',
                        help="Specify the path to save wav files.")
arg_parser.add_argument("-i", action='store', type=str, dest='pathToInfo',
                        help="Specify the path to save information about files.")
def main():

    args = arg_parser.parse_args()

    if not args.pathToXml:
        print "Set the flag -p /path/to/xml"
        return 1

    if not os.path.exists(args.pathToXml):
        print "Path to xml not exists :", args.pathToXml
        return 1

    if not os.path.exists(args.pathToSave):
        # print "Path to save not exists :", args.pathToSave
        os.mkdir(args.pathToSave)

    if not args.pathToInfo:
        print "Not specified file for utterance info. -i", args.pathToInfo


    file_info = codecs.open(args.pathToInfo,'w', encoding='utf8')

    file_xml = os.path.join (args.pathToXml)

    tree = et.ElementTree(file=file_xml)
    rootNode = tree.getroot()

    dict = {} # id:rawPath
    for child in rootNode.iter('AudioRoot'):
        dict[child.attrib['id']] = child.attrib['rawPath']


    for child in rootNode.iter('Utt'):
        if child.attrib['transcribe'] == 'yes':
            os.system("cp %s%s %s" %  (dict[child.attrib['audioRoot']], child.attrib['audio'], args.pathToSave))
            confidence = (int(child.attrib['conf']) + 0.0) / 1000
            file_info.write('%s;%s;%s;%f\n' % (child.attrib['audio'], child.attrib['rawText'], child.attrib['recValue'], confidence))

if __name__ == '__main__':
    main()