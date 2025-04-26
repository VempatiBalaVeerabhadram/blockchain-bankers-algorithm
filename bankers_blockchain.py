import random
import time
from collections import deque

class BlockchainBankersAlgorithm:
    def __init__(self, resources, nodes):
        self.resources = resources
        self.nodes = nodes
        self.allocation = [[0] * len(resources) for _ in range(nodes)]
        self.maximum = [[0] * len(resources) for _ in range(nodes)]
        self.need = [[0] * len(resources) for _ in range(nodes)]
        self.available = resources[:]
        self.transaction_queue = [deque() for _ in range(nodes)]
       
    def request_resources(self, node_id, request):
        """Request resources for a node."""
        for i in range(len(request)):
            if request[i] > self.need[node_id][i] or request[i] > self.available[i]:
                return False
        # Temporarily allocate resources
        temp_available = self.available[:]
        temp_allocation = [row[:] for row in self.allocation]
        temp_need = [row[:] for row in self.need]
        for i in range(len(request)):
            self.available[i] -= request[i]
            self.allocation[node_id][i] += request[i]
            self.need[node_id][i] -= request[i]
        if self.is_safe():
            return True
        # Rollback if unsafe
        self.available = temp_available
        self.allocation = temp_allocation
        self.need = temp_need
        return False

    def release_resources(self, node_id):
        """Release resources from a node."""
        for i in range(len(self.resources)):
            self.available[i] += self.allocation[node_id][i]
            self.allocation[node_id][i] = 0
            self.need[node_id][i] = self.maximum[node_id][i]
       
    def is_safe(self):
        """Check if the system is in a safe state."""
        work = self.available[:]
        finish = [False] * self.nodes
        while False in finish:
            progress_made = False
            for i in range(self.nodes):
                if not finish[i] and all(self.need[i][j] <= work[j] for j in range(len(self.resources))):
                    for j in range(len(self.resources)):
                        work[j] += self.allocation[i][j]
                    finish[i] = True
                    progress_made = True
                    break
            if not progress_made:
                return False
        return True

    def simulate_transactions(self):
        for _ in range(5):  # << run 5 rounds
            for i in range(self.nodes):
                request = []
                for j in range(len(self.resources)):
                    max_request = max(0, self.need[i][j])
                    request.append(random.randint(0, max_request))
                self.transaction_queue[i].append(request)
        
        for i in range(self.nodes):
            while self.transaction_queue[i]:
                request = self.transaction_queue[i].popleft()
                print(f"Node {i} requesting resources: {request}")
                if self.request_resources(i, request):
                    print(f"✅ Request granted for Node {i}.")
                    time.sleep(0.5)  # Faster
                    self.release_resources(i)
                    print(f"🔄 Node {i} released resources.")
                else:
                    print(f"❌ Request denied for Node {i}.")
                time.sleep(0.5)

def main():
    # Example usage
    resources = [10, 5, 7]  # Total resources (e.g., CPU, memory, storage)
    nodes = 3  # Number of nodes (blockchain validators)
   
    blockchain = BlockchainBankersAlgorithm(resources, nodes)
   
    # Maximum resources needed by each node
    blockchain.maximum[0] = [7, 5, 3]
    blockchain.maximum[1] = [3, 2, 2]
    blockchain.maximum[2] = [9, 3, 6]  # <-- corrected here
   
    # Initial allocation of resources
    blockchain.allocation[0] = [2, 1, 1]
    blockchain.allocation[1] = [2, 1, 1]
    blockchain.allocation[2] = [3, 2, 2]
   
    # Calculate the need matrix
    for i in range(nodes):
        for j in range(len(resources)):
            blockchain.need[i][j] = blockchain.maximum[i][j] - blockchain.allocation[i][j]
   
    # Simulate transaction processing
    blockchain.simulate_transactions()

if __name__ == "__main__":
    main()
