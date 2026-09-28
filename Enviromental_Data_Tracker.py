# ------------------------------------
# Date helpers
# ------------------------------------

#Takes a date MM DD Y, splits it and returns it as a compareable tuple
def parse_date(date_str):
    month, day, year = date_str.split("-")
    return (int(year), int(month), int(day))


def format_date(date_tuple):
    #Turns (2026, 1, 4) back into "01-04-2026"
    # Unpack the tuple.
    year, month, day = date_tuple
    # Rebuild it as MM-DD-YYYY text.
    return f"{month:02d}-{day:02d}-{year}"

# ---------------------------------------------------------------------
# DataNode: Node which holds the location, temperature value and date
# ---------------------------------------------------------------------

class DataNode:
    def __init__(self, location, value, date_str):
        self.location = location
        self.value = float(value)
        self.date = parse_date(date_str)
        self.next = None

# ------------------------------------------------------------------
# DataList: the linked list, holds the head, min and max
# ------------------------------------------------------------------

class DataList:
    def __init__(self):
        self.head = None
        self.min_node = None
        self.max_node = None

    #Iterates through each node in the linked list from head to tail. Allows the use of for loops: "for node in linked_list"
    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next

    #Goes through the whole list to find current min and max
    def _refresh_min_max(self):
        self.min_node = None
        self.max_node = None
        for node in self:
            if self.max_node is None or node.value > self.max_node.value:
                self.max_node = node
            if self.min_node is None or node.value < self.min_node.value:
                self.min_node = node

    #Insert a new reading in chronological date order
    def insert(self, location, value, date_str):
        new_node = DataNode(location, value, date_str)

        # New node becomes the new first node if it is the first entry or most recent date 
        if self.head is None or new_node.date < self.head.date:
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            # Walk forward to find the right index
            while current.next is not None and current.next.date <= new_node.date:
                current = current.next
            # Splice the new node in after "current"
            new_node.next = current.next
            current.next = new_node

        # Update min/max right away instead of rescanning the whole list
        if self.max_node is None or new_node.value > self.max_node.value:
            self.max_node = new_node
        if self.min_node is None or new_node.value < self.min_node.value:
            self.min_node = new_node

    # Show all readings
    def display(self):
        for node in self:
            print(f"[{format_date(node.date)}] {node.location}: {node.value}")

    # Shows whether each location's value went up, down, or stayed the same
    def display_trends(self):
        # Remembers the previous value seen for each location
        last_value_by_location = {}
        for node in self:
            if node.location not in last_value_by_location:
                # No history yet
                trend = "first reading"
            elif node.value > last_value_by_location[node.location]:
                # Went up since last time
                trend = "increasing"
            elif node.value < last_value_by_location[node.location]:
                # Went down since last time
                trend = "decreasing"
            else:
                # Same as last time
                trend = "stable"

            print(f"[{format_date(node.date)}] {node.location}: {node.value}  ({trend})")
            # Update the memory.
            last_value_by_location[node.location] = node.value

    #Remove readings older than a given date
    def remove_older_than(self, cutoff_str):
        cutoff = parse_date(cutoff_str)
        removed_count = 0

        # Remove old nodes from the very front of the list
        while self.head is not None and self.head.date < cutoff:
            self.head = self.head.next
            removed_count += 1

        # Remove old nodes from the middle/end of the list
        current = self.head
        while current is not None and current.next is not None:
            if current.next.date < cutoff:
                # Skip over the outdated node.
                current.next = current.next.next
                removed_count += 1
            else:
                # Move forward as normal
                current = current.next

        if removed_count > 0:
            #Recheck min & max in case one of them was removed
            self._refresh_min_max()

        return removed_count

    #Merge two lists together and remove duplicates
    def merge_and_deduplicate(self, other_list):
        # two pointer merge directly on the nodes
        dummy = DataNode("TEMP", 0, "01-01-2000")
        tail = dummy
        p1, p2 = self.head, other_list.head
        seen = set()

        while p1 or p2:
            # Pick the earlier node
            if not p2 or (p1 and p1.date <= p2.date):
                chosen = p1
                p1 = p1.next
            else:
                chosen = p2
                p2 = p2.next

            key = (chosen.location, chosen.date, chosen.value)
            if key not in seen:
                seen.add(key)
                tail.next = chosen
                tail = tail.next

        tail.next = None
        self.head = dummy.next
        other_list.head = None
        self._refresh_min_max()

    #Find the max and min recorded values
    def find_max(self):
        return self.max_node

    def find_min(self):
        return self.min_node

    #Moving average over a window of readings
    def moving_average(self, window_size):
        values = [node.value for node in self]
        if window_size <= 0 or len(values) < window_size:
            # Not enough data
            return []

        averages = []
        for i in range(len(values) - window_size + 1):
            # The next window size values.
            window = values[i:i + window_size]
            averages.append(sum(window) / window_size)
        return averages

    #Detect sudden spikes / anomalies
    # Compares each reading to the average of the readings just before it
    # If it's more than 2 standard deviations away it gets flagged
    def detect_anomalies(self, window_size, threshold=2.0):
        nodes = list(self)
        anomalies = []

        # Skip the first window, since there is nothing to compare it with
        for i in range(window_size, len(nodes)):
            window_values = [nodes[j].value for j in range(i - window_size, i)]

            #Recent value
            mean = sum(window_values) / window_size
            variance = sum((v - mean) ** 2 for v in window_values) / window_size
            # How spread out they are.
            stddev = variance ** 0.5

            if stddev < 1e-6:
                # All values in the window were the same; skip it.
                continue

            #Calculates how unusal the point is
            deviation = abs(nodes[i].value - mean) / stddev
            if deviation >= threshold:
                # Flag it as an anomaly
                anomalies.append((nodes[i], mean, deviation))

        return anomalies

    #Search for a location within a date range
    def search(self, location, start_str, end_str):
        # Earliest date
        start = parse_date(start_str)
        # Latest date
        end = parse_date(end_str)

        results = []
        for node in self:
            # The list is kept sorted by date, so once we pass the end of
            # the range nothing further along can match either - stop early
            # instead of scanning the rest of the list.
            if node.date > end:
                break
            if node.location == location and start <= node.date <= end:
                # Matches both the place and the date range.
                results.append(node)
        return results