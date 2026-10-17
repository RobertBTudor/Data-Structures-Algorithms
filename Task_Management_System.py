# ---------------------------------------------------------------------------
# TaskNode: one single task in the list
# ---------------------------------------------------------------------------
class TaskNode:
    def __init__(self, description, category, deadline, priority):
        # Checks to avoudcreating a task with bad data
        if priority not in (1, 2, 3):
            raise ValueError("priority must be 1 (High), 2 (Medium), or 3 (Low)")
        if not (10000101 <= deadline <= 99991231):
            raise ValueError("deadline must be a number formatted like YYYYMMDD")

        self.description = description      
        self.category = category            
        self.deadline = deadline            
        self.priority = priority            
        self.completed = False              

        self.prev = None                   
        self.next = None              

    def priority_label(self):
        # Turns the number into a word
        if self.priority == 1:
            return "High"
        elif self.priority == 2:
            return "Medium"
        else:
            return "Low"

    def __repr__(self):
        #Controls how the task looks when printed
        status = "DONE" if self.completed else "OPEN"
        return "[{}] ({}, due {}) {} <{}>".format(
            status, self.priority_label(), self.deadline, self.description, self.category
        )


# --------------------------------------------------------------------
# TaskList: the doubly linked list that holds all the TaskNodes
# --------------------------------------------------------------------
class TaskList:
    def __init__(self):
        self.head = None   
        self.tail = None      
        self.size = 0         
        self.cursor = None     

    # ------------------------------------------------------------------
    # Add a task, keeping the list sorted by priority then deadline
    # ------------------------------------------------------------------
    def insert_task(self, description, category, deadline, priority):
        new_node = TaskNode(description, category, deadline, priority)

        #list is empty, so the new task becomes head and tail
        if self.head is None:
            self.head = new_node
            self.tail = new_node

        else:
            #Places task in order of urgency
            current = self.head
            while current is not None and self.more_urgent_or_equal(current, new_node):
                current = current.next

            if current is None:
                # We walked off the end, so the new task goes at the tail
                new_node.prev = self.tail
                self.tail.next = new_node
                self.tail = new_node

            elif current.prev is None:
                # The new task is more urgent than everything, goes at the front
                new_node.next = self.head
                self.head.prev = new_node
                self.head = new_node

            else:
                # Insert new_node in the middle, right before "current"
                before = current.prev
                before.next = new_node
                new_node.prev = before
                new_node.next = current
                current.prev = new_node

        self.size += 1

        #Starts the cursor at the head if none
        if self.cursor is None:
            self.cursor = self.head

        return new_node

    def more_urgent_or_equal(self, task_a, task_b):
        # Returns True if task_a <= task_b
        # Compares priority first, then deadline if priorities match
        if task_a.priority != task_b.priority:
            return task_a.priority < task_b.priority
        return task_a.deadline <= task_b.deadline

    # ------------------------------------------------------------------
    # Display all tasks, sorted by priority
    # ------------------------------------------------------------------
    def display_all(self, include_completed=True):
        if self.head is None:
            print("No tasks in the list.")
            return

        count = 1
        current = self.head
        while current is not None:
            if include_completed or not current.completed:
                print(str(count) + ". " + str(current))
                count += 1
            current = current.next

    def to_list(self):
        # Returns all the tasks as a normal python list
        result = []
        current = self.head
        while current is not None:
            result.append(current)
            current = current.next
        return result

    # -------------------------------------------
    # Search for tasks that contain a keyword
    # -------------------------------------------
    def search_by_keyword(self, keyword):
        keyword = keyword.lower()
        matches = []
        current = self.head
        while current is not None:
            description_match = keyword in current.description.lower()
            category_match = keyword in current.category.lower()
            if description_match or category_match:
                matches.append(current)
            current = current.next
        return matches

    # ----------------------------------------------------------------
    # Mark tasks as completed, and remove completed tasks
    # ---------------------------------------------------------------
    def mark_completed(self, description):
        current = self.head
        while current is not None:
            if current.description.lower() == description.lower():
                current.completed = True
                return True
            current = current.next
        return False

    def remove_node(self, node):
        if node.prev is not None:
            node.prev.next = node.next
        else:
            # node was the head, so the next node becomes the new head
            self.head = node.next

        if node.next is not None:
            node.next.prev = node.prev
        else:
            # node was the tail, so the previous node becomes the new tail
            self.tail = node.prev

        # If the cursor was pointing at the node we're removing, move it
        if self.cursor is node:
            if node.next is not None:
                self.cursor = node.next
            else:
                self.cursor = node.prev

        node.prev = None
        node.next = None
        self.size -= 1

    def remove_completed_tasks(self):
        removed_count = 0
        current = self.head
        while current is not None:
            next_node = current.next 
            if current.completed:
                self.remove_node(current)
                removed_count += 1
            current = next_node
        return removed_count

    def remove_task(self, description):
        current = self.head
        while current is not None:
            if current.description.lower() == description.lower():
                self.remove_node(current)
                return True
            current = current.next
        return False

    # ------------------------------------------------------------------
    # Navigate through the list forward and backward using a cursor
    # ------------------------------------------------------------------
    def reset_cursor(self):
        # Moves the cursor back to the first task
        self.cursor = self.head
        return self.cursor

    def current_task(self):
        return self.cursor

    def next_task(self):
        # Moves the cursor one step forward and returns the new task
        if self.cursor is None:
            self.cursor = self.head
        elif self.cursor.next is not None:
            self.cursor = self.cursor.next
        else:
            return None
        return self.cursor

    def previous_task(self):
        # Moves the cursor one step backward and returns the new task
        if self.cursor is None:
            self.cursor = self.tail
        elif self.cursor.prev is not None:
            self.cursor = self.cursor.prev
        else:
            return None
        return self.cursor

    # ------------------------------
    # Advanced features
    # -------------------------------
    def find_most_urgent_task(self):
        #The most urgent task is alwasys the first one since the list is sorted
        current = self.head
        while current is not None:
            if not current.completed:
                return current
            current = current.next
        return None

    def filter_by_category(self, category, include_completed=True):
        category = category.lower()
        results = []
        current = self.head
        while current is not None:
            same_category = current.category.lower() == category
            if same_category and (include_completed or not current.completed):
                results.append(current)
            current = current.next
        return results


# -------------------------------------------------------------
# Menu for interacting with the TaskList
# -------------------------------------------------------------
def print_menu():
    print("\n----- TASK MENU -----")
    print("1. Insert a new task")
    print("2. Display all tasks (sorted by priority)")
    print("3. Search for a task by keyword")
    print("4. Remove completed tasks")
    print("5. Find the most urgent task")
    print("6. Filter tasks by category")
    print("7. Mark a task as completed")
    print("8. Quit")


def ask_for_new_task():
    # Gathers the details needed for insert_task() from the user.
    # Returns None if the user typed something invalid.
    description = input("Task description: ")
    category = input("Category (e.g. Work, Personal, Study): ")

    deadline_text = input("Deadline (YYYYMMDD, e.g. 20260805): ")
    try:
        deadline = int(deadline_text)
    except ValueError:
        print("That deadline wasn't a valid number. Task not added.")
        return None

    priority_text = input("Priority (1 = High, 2 = Medium, 3 = Low): ")
    try:
        priority = int(priority_text)
    except ValueError:
        print("That priority wasn't a valid number. Task not added.")
        return None

    return description, category, deadline, priority


def run_menu():
    tasks = TaskList()

    while True:
        print_menu()
        choice = input("Choose an option (1-8): ")

        if choice == "1":
            new_task_details = ask_for_new_task()
            if new_task_details is not None:
                description, category, deadline, priority = new_task_details
                try:
                    tasks.insert_task(description, category, deadline, priority)
                    print("Task added!")
                except ValueError as error:
                    print("Could not add task: " + str(error))

        elif choice == "2":
            print("\n--- All Tasks (sorted by priority) ---")
            tasks.display_all()

        elif choice == "3":
            keyword = input("Enter a keyword to search for: ")
            results = tasks.search_by_keyword(keyword)
            if len(results) == 0:
                print("No tasks matched that keyword.")
            else:
                print("\n--- Matching Tasks ---")
                for task in results:
                    print(task)

        elif choice == "4":
            removed = tasks.remove_completed_tasks()
            print("Removed " + str(removed) + " completed task(s).")

        elif choice == "5":
            urgent_task = tasks.find_most_urgent_task()
            if urgent_task is None:
                print("There are no open tasks right now.")
            else:
                print("\n--- Most Urgent Task ---")
                print(urgent_task)

        elif choice == "6":
            category = input("Enter a category to filter by: ")
            results = tasks.filter_by_category(category)
            if len(results) == 0:
                print("No tasks found in that category.")
            else:
                print("\n--- Tasks in category '" + category + "' ---")
                for task in results:
                    print(task)

        elif choice == "7":
            description = input("Enter the exact description of the task to mark complete: ")
            found = tasks.mark_completed(description)
            if found:
                print("Task marked as completed.")
            else:
                print("No task with that description was found.")

        elif choice == "8":
            print("Goodbye!")
            break

        else:
            print("That's not a valid option, please choose 1-8.")


if __name__ == "__main__":
    run_menu()