from IPython.display import IFrame
import json
import uuid

def draw(graph, options):
    # This will draw your ENTIRE GRAPH; be careful! It's intended to be used with small, example datasets.
    # The options argument should be a dictionary of node labels and property keys; it determines which property 
    # is displayed for the node label. For example, in the movie graph, options = {"Movie": "title", "Person": "name"}.
    query = """
    MATCH n
    OPTIONAL MATCH (n)-[r]->(m)
    RETURN n, r, m
    """

    data = graph.cypher.execute(query)

    nodes = []
    edges = []

    def get_vis_info(node):
        node_label = list(node.labels)[0]
        prop_key = options[node_label]
        vis_label = node.properties[prop_key]

        title = {}

        for key, value in node.properties.items():
            key = key.encode("utf8")
            value = value.encode("utf8") if type(value) is unicode else value

            title[key] = value

        return {"id": vis_label, "label": vis_label, "group": node_label, "title": repr(title)}

    for row in data:
        source = row[0]
        rel = row[1]
        target = row[2]

        source_info = get_vis_info(source)

        if source_info not in nodes:
            nodes.append(source_info)

        if rel:
            target_info = get_vis_info(target)

            if target_info not in nodes:
                nodes.append(target_info)

            edges.append({"from": source_info["id"], "to": target_info["id"], "label": rel.type})
            
    html = """
    <html>
    <head>
      <script type="text/javascript" src="../lib/vis/dist/vis.js"></script>
      <link href="../lib/vis/dist/vis.css" rel="stylesheet" type="text/css">
    </head>
    <body>

    <div id="{id}"></div>

    <script type="text/javascript">
      var nodes = {nodes};
      var edges = {edges};

      var container = document.getElementById("{id}");
      
      var data = {{
        nodes: nodes,
        edges: edges
      }};
      
      var options = {{
          nodes: {{
              shape: 'dot',
              size: 25,
              font: {{
                  size: 14
              }}
          }},
          edges: {{
              font: {{
                  size: 14,
                  align: 'middle'
              }},
              color: 'gray',
              arrows: {{
                  to: {{enabled: true, scaleFactor: 0.5}}
              }},
              smooth: {{enabled: false}}
          }},
          physics: {{
              enabled: false
          }}
      }};
      
      var network = new vis.Network(container, data, options);

    </script>
    </body>
    </html>
    """

    unique_id = str(uuid.uuid4())
    html = html.format(id=unique_id, nodes=json.dumps(nodes), edges=json.dumps(edges))
    
    filename = "figure/graph-{}.html".format(unique_id)

    file = open(filename, "w")
    file.write(html)
    file.close()

    return IFrame(filename, width="500", height="300")