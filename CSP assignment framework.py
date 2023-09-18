#This is a framework by which a CSP based model couls be achieved


from constraint import Problem

# A function which calculates the total of parcel values assigned to an agent
def calculate_agent_capacity(parcel_list, assignments, agent_id):
    capacity = 0
    for parcel_index in range(len(assignments)):
        if assignments[parcel_index] == agent_id:
            capacity += parcel_list[parcel_index]
    return capacity


class DeliveryAgent:
    def __init__(self, agent_id, capacity):
        # Initialize a delivery agent with an agent ID and capacity.
        self.agent_id = agent_id
        self.capacity = capacity
        self.route = []  # Initialize an empty route for the agent.

    def submit_capacity(self):
        # When requested, submit the agent's capacity to the Master Routing Agent (MRA).
        return self.capacity








class MasterRoutingAgent:
    def __init__(self, delivery_agents):
        # Initialize the Master Routing Agent with a list of delivery agents.
        self.delivery_agents = delivery_agents
        self.parcel_list = []  # Initialize an empty list for parcels to be delivered.
        self.routes = {}  # Initialize an empty dictionary to store route assignments.

    def collect_capacity_constraints(self):
        # Collect capacity constraints from all delivery agents.
        capacities = [agent.submit_capacity() for agent in self.delivery_agents]
        return capacities

    def receive_parcel_list(self, parcels):
        # Receive the list of parcels to be delivered.
        self.parcel_list = parcels

    def generate_routes(self):
        # Create a CSP problem instance
        problem = Problem()

        # Add variables for each parcel to assign to a delivery agent
        parcel_variables = [f'parcel_{i}' for i in range(len(self.parcel_list))]
        for parcel_var in parcel_variables:
            problem.addVariable(parcel_var, list(self.routes.keys()))

        # Add capacity constraints to the CSP
        capacities = self.collect_capacity_constraints()

        for agent_id, route_info in self.routes.items():
            agent_capacity = route_info["capacity"]

            def capacity_constraint(*parcels):
                assigned_agent_capacity = calculate_agent_capacity(self.parcel_list, parcels, agent_id)
                return assigned_agent_capacity <= agent_capacity

            problem.addConstraint(capacity_constraint, parcel_variables)

        # Find a solution that satisfies the CSP
        solutions = problem.getSolutions()

        # Update the routes based on the CSP solution
        for solution in solutions:
            agent_routes = {agent_id: [] for agent_id in self.routes.keys()}
            for parcel_var, agent_id in solution.items():
                parcel_index = int(parcel_var.split('_')[1])
                agent_routes[agent_id].append(self.parcel_list[parcel_index])
            self.routes = agent_routes

# ...

if __name__ == "__main__":

    #this part could be automised these are test values


    # Creates delivery agents with Id's and capacity counts
    da1 = DeliveryAgent(agent_id=1, capacity=10)
    da2 = DeliveryAgent(agent_id=2, capacity=15)

    # Create MRA with a list of delivery agents.
    mra = MasterRoutingAgent(delivery_agents=[da1, da2])

    # Define a list of parcels/items to be delivered.
    parcel_list = ["Parcel A", "Parcel B", "Parcel C", "Parcel D", "Parcel E"]

    # Collect capacity constraints from agents.
    mra.collect_capacity_constraints()

    # Receive the parcel list.
    mra.receive_parcel_list(parcel_list)

    # Generate and assign routes using the CSP-based approach
    mra.generate_routes()

    # Notify agents of their routes
    mra.notify_agents_of_routes()
