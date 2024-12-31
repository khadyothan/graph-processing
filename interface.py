from neo4j import GraphDatabase


class Interface:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(
            uri, auth=(user, password), encrypted=False)
        self._driver.verify_connectivity()

    def close(self):
        self._driver.close()

    def initialize_graph_projection(self):
        graph_name = "myGraph"
        node_label = "Location"
        relationship = "TRIP"
        properties = ['distance', 'fare']

        with self._driver.session() as session:
            session.run(
                """
                CALL gds.graph.drop($graph_name, false) YIELD graphName
                """,
                graph_name=graph_name
            )
            session.run(
                """
                CALL gds.graph.project(
                    $graph_name,
                    $node_label,
                    $relationship,
                    {
                        relationshipProperties: $properties
                    }
                )
                """,
                graph_name=graph_name,
                node_label=node_label,
                relationship=relationship,
                properties=properties
            )

    def bfs(self, start_node, last_node):
        # TODO: Implement this method
        self.initialize_graph_projection()
        with self._driver.session() as session:
            query = """
                MATCH (source:Location {name: $start_id}), (destination:Location {name: $end_id})
                WITH source AS sourceNode, destination AS destinationNode
                CALL gds.bfs.stream($graph_name, {
                    sourceNode: sourceNode,
                    targetNodes: [destinationNode]
                })
                YIELD path
                RETURN [node IN nodes(path) | {name: node.name}] AS route
                LIMIT 1
            """
            result = session.run(
                query,
                graph_name="myGraph",
                start_id=start_node,
                end_id=last_node
            )
            routes = result.single()
            return [{"path": routes["route"]}] if routes else [{"path": []}]

    def pagerank(self, max_iterations, weight_property):
        # TODO: Implement this method
        self.initialize_graph_projection()
        with self._driver.session() as session:
            query = """
                CALL gds.pageRank.stream($graph_name, {
                    maxIterations: $max_iterations,
                    relationshipWeightProperty: $weight_property
                })
                YIELD nodeId, score
                RETURN gds.util.asNode(nodeId).name AS name, score
                ORDER BY score DESC
            """

            result = session.run(
                query,
                graph_name="myGraph",
                max_iterations=max_iterations,
                weight_property=weight_property
            )

            results = list(result)
            if results:
                return [{"name": int(results[0]["name"]), "score": results[0]["score"]}, {"name": int(results[-1]["name"]), "score": results[-1]["score"]}]
            else:
                return [{"name": None, "score": None}, {"name": None, "score": None}]
