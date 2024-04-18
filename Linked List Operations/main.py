"""
This Python program demonstrates the use of linked lists to perform various operations such as appending, sorting, and deleting data. It also measures the time taken for these operations and writes the cumulative sum of the data to CSV files. The program utilizes different types of linked lists: SinglyLinkedList, DoublyLinkedList, and CircularDoublyLinkedList. It reads data from CSV files, sorts it, performs insertions, and deletes elements based on provided indices.
"""

import csv
import time

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, value):
        new_node = Node(value)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def to_list(self):
        return [node.value for node in self._iterate()]

    def _iterate(self):
        current = self.head
        while current:
            yield current
            current = current.next

class DoublyLinkedList(SinglyLinkedList):
    # Inherits from SinglyLinkedList and uses the same append method

    def to_list(self):
        return [node.value for node in self._iterate()]

class CircularDoublyLinkedList(DoublyLinkedList):
    # Inherits from DoublyLinkedList and overrides the append method

    def append(self, value):
        new_node = Node(value)
        if not self.head:
            self.head = new_node
            self.head.next = self.head
            self.head.prev = self.head
            self.tail = self.head
        else:
            new_node.prev = self.tail
            new_node.next = self.head
            self.tail.next = new_node
            self.head.prev = new_node
            self.tail = new_node

def cumulative_sum(data):
    total = 0
    for value in data:
        total += value
        yield total

def read_data(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        return [float(row[0]) for row in reader]

def write_cumulative_sum_to_csv(data, file_path):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Index', 'Cumulative Sum'])
        for i, total in enumerate(cumulative_sum(data), 1):
            writer.writerow([i, total])



def main():
    original_file_path = 'orginaldata.csv'
    inserted_file_path = 'inserteddata.csv'
    delete_index_file = "deleteindex.csv"

    linked_lists = [SinglyLinkedList(), DoublyLinkedList(), CircularDoublyLinkedList()]
    output_paths = ['outputs', 'outputs', 'outputs']
    output_files = ['sorted_file.csv', 'insert_file.csv', 'delete_file.csv']

    for i, linked_list in enumerate(linked_lists):
        # Read original data and append to the linked list
        with open(original_file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                for value in map(float, row):
                    linked_list.append(value)

        # Measure original data sorting time and calculate its cumulative sum
        start_time_sorting = time.time()
        original_data = linked_list.to_list()
        original_data.sort()  # Sort the original data
        cumulative_original_data = cumulative_sum(original_data)
        end_time_sorting = time.time()
        sorting_time = end_time_sorting - start_time_sorting

        # Measure insertion time in sorted original data
        start_time_insertion = time.time()
        merged_data = original_data[:]

        # Read inserted data and append to the list
        with open(inserted_file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                for value in map(float, row):
                    merged_data.append(value)

        merged_data.sort()  # Sort the merged data
        end_time_insertion = time.time()
        insertion_time = end_time_insertion - start_time_insertion

        # Measure deletion index time in sorted and inserted original data
        start_time_deletion = time.time()
        merged_data_with_deletion = merged_data[:]
        with open(delete_index_file, 'r') as file:
            reader = csv.reader(file)
            delete_indexes = [int(row[0]) - 1 for row in reader]  # Convert to 0-based indexing
        for index in delete_indexes:
            del merged_data_with_deletion[index]
        end_time_deletion = time.time()
        deletion_time = end_time_deletion - start_time_deletion

        # Write cumulative sum files
        write_cumulative_sum_to_csv(cumulative_original_data, output_paths[i] + output_files[0])
        write_cumulative_sum_to_csv(merged_data, output_paths[i] + output_files[1])
        write_cumulative_sum_to_csv(merged_data_with_deletion, output_paths[i] + output_files[2])

        total_time = sorting_time + insertion_time + deletion_time
        # Print the timing results
        print(f"Original Data Sorting Time for {type(linked_list)._name_}: {sorting_time:.4f} ")
        print(f"Insertion Time in Sorted Original Data for {type(linked_list)._name_}: {insertion_time:.4f} ")
        print(f"Deletion Index Time in Sorted and Inserted Original Data for {type(linked_list)._name_}: {deletion_time:.4f} ")
        print(f"Original Data Total Time for {type(linked_list)._name_}: {total_time:.4f} ")

if __name__ == "_main_":
    main()