#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import tempfile
import heapq
import sys
import json

class heapnode:

    def __init__(
            self,
            item,
            fileHandler,
    ):
        self.item = item
        self.fileHandler = fileHandler


class externalMergeSort:

    def __init__(self):
        self.sortedTempFileHandlerList = []
        self.getCurrentDir()

    def getCurrentDir(self):
        self.cwd = os.getcwd()

    def iterateSortedData(self, sortedCompleteData):
        for element in sortedCompleteData:
            print(element)

    def strcom(self, str1, str2):
        arr = [str1, str2]
        arr.sort(key=str.lower)
        if str1 == arr[0]:
            return True
        else:
            return False

    def mergeSortedtempFiles(self):
        mergedStr = (map(str, tempFileHandler) for tempFileHandler in
                    self.sortedTempFileHandlerList)
        sortedCompleteData = heapq.merge(*mergedStr)
        return sortedCompleteData

    def heapify(
            self,
            arr,
            i,
            n,
    ):
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and self.strcom(arr[left].item.name, arr[i].item.name):
            smallest = left
        else:
            smallest = i

        if right < n and self.strcom(arr[right].item.name, arr[smallest].item.name):
            smallest = right

        if i != smallest:
            (arr[i], arr[smallest]) = (arr[smallest], arr[i])
            self.heapify(arr, smallest, n)

    def construct_heap(self, arr):
        l = len(arr) - 1
        mid = l / 2
        while mid >= 0:
            self.heapify(arr, mid, l)
            mid -= 1

    def mergeSortedtempFiles_low_level(self):
        list = []
        sorted_output = []
        for tempFileHandler in self.sortedTempFileHandlerList:
            item = json.loads(tempFileHandler.readline().strip())
            list.append(heapnode(item, tempFileHandler))

        self.construct_heap(list)
        while True:
            min = list[0]
            if min.item == sys.maxsize:
                break
            sorted_output.append(min.item)
            fileHandler = min.fileHandler
            item = json.loads(fileHandler.readline().strip())
            if not item:
                item = sys.maxsize
            else:
                item = json.loads(item)
            list[0] = heapnode(item, fileHandler)
            self.heapify(list, 0, len(list))
        return sorted_output

    def splitFiles(self, largeFileName, smallFileSize):
        largeFileHandler = open(largeFileName)
        tempBuffer = []
        size = 0
        while True:
            line = largeFileHandler.readline()
            if not line:
                break
            line = line.strip()
            json_obj = json.loads(line)
            # lines.append(json_obj)
            tempBuffer.append(json_obj)
            size += 1
            if size % smallFileSize == 0:
                tempBuffer = sorted(tempBuffer, key=lambda k: k['name'])
                tempFile = tempfile.NamedTemporaryFile(dir='\\temp', delete=False)
                if tempFile:
                    # Writing JSON data
                    with open(tempFile, 'w') as f:
                        json.dump(tempBuffer, f)
                # tempFile.writelines(tempBuffer)
                tempFile.seek(0)
                self.sortedTempFileHandlerList.append(tempFile)
                tempBuffer = []


if __name__ == '__main__':
    largeFileName = 'Sample.jsonrows'
    smallFileSize = 10
    obj = externalMergeSort()
    obj.splitFiles(largeFileName, smallFileSize)
    """ Useslower level functions without any python Libraries . Better to understand it """
    print(obj.mergeSortedtempFiles_low_level())
    """Pythonic way - Uses a generator """
# sortedCompleteData = obj.mergeSortedtempFiles()
# obj.iterateSortedData(sortedCompleteData)
