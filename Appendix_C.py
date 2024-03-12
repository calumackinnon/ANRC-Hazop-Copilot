if __name__ == '__main__':
	# === save all ontologies
	ontology_operations.save_ontology()
	ontology_operations.save_ontology_as_sql()
	upper_onto.determine_onto()

	start_time = time.time()
	# === Process model
	process_plant_model = model.create_hazid_benchmark_1()
	
	deviation_number = None
	stack_elements = []
	
	# === Tearing strategy/strategy for defining order of process equipment/start-end point
	if len(process_plant_model.nodes) > 1:
		graph_type, newly_arranged_graphs, intersections = algorithm.determine_propagation_strategy(process_plant_model)
	print(list(newly_arranged_graphs))

	if config.EQUIPMENT_BASED_EVALUATION:
		for index in range(len(process_plant_model.nodes)):
			equipment_specific_prop_scenarios = []
			
			equipment_entity = process_plant_model.nodes[index]["data"]
			# Add port information to equipment entity
			for key, value in process_plant_model.nodes[index]["ports"].items():
				equipment_entity.onto_object.hasPort.append(value.onto_object)
				# Add port information to equipment entity
				if value.port_instrumentation:
					equipment_entity.onto_object.hasInstrumentation.append(value.port_instrumentation)
			
			process_unit_obj = equipment_entity.onto_object.is_a[0]
			
			# === continue in case of source and sink, since they are not relevant in
			# equipment-based mode to save reasoner calls
			if process_unit_obj == equipment_onto.SinkEntity:
				continue
			
			substances = process_plant_model.nodes[index]["substances"]
			environment = process_plant_model.nodes[index]["environment"]
			deviations = config.deviation_selector(process_unit_obj)
			
			# === Infer hazards
			infer.equipment_based_analysis(equipment_entity,
											deviations,
											substances,
											environment,
											equipment_specific_prop_scenarios)
			
			stack_elements.append({"{0}".format(equipment_entity.name): equipment_entity,
									pre_processing.DictName.scenario: equipment_specific_prop_scenarios})

	# === Entry point for hazard/malfunction propagation
	if config.PROPAGATION_BASED_EVALUATION:
		if graph_type == algorithm.GraphType.SingleLineSystem:
			infer.propagation_based_analysis(process_plant_model, newly_arranged_graphs, stack_elements)
		
		elif graph_type == algorithm.GraphType.MultiCycleSystem:
			for index, cycle in enumerate(newly_arranged_graphs):
				# intersection of cycles
				intersection_node_index = cycle.index(intersections)
				
				# start first cycle one node after intersection and following nodes at intersection
				if index == 0:
					intersection_node_index += 1

				# === Change order of graph [intersection + 1] as starting node
				new_order = []
				for node in go.starting_with(cycle, intersection_node_index):
					new_order.append(node)
				
				infer.propagation_based_analysis(process_plant_model,
												new_order,
												stack_elements)
		
		elif graph_type == algorithm.GraphType.JunctionSystem or \
				graph_type == algorithm.GraphType.ComplexSystem or \
				graph_type == algorithm.GraphType.RecycleFlowSystem:
			for stream in newly_arranged_graphs:
				infer.propagation_based_analysis(process_plant_model, stream, stack_elements)
		else:
			print("Case not covered by any strategy!")

	# === remove duplicates and sort results table
	results = pre_processing.cleanup_result_list(results)
	results = sorted(results, key=lambda k: k["process_equipment_id"])

	# === Hazop table
	if results:
		counter = 0
			for row in results:
				if row["cause"] or row["effect"] or row["consequence"]:
					output.hazop_table.add_row([counter,
												row["process_equipment"],
												row["process_equipment_id"],
												', '.join(row["operation_mode"]),
												row["substance"],
												', '.join(row["deviation"]),
											', '.join(row["super_cause"]),
											', '.join(row["cause"]),
											', '.join(row["effect"]),
											', '.join(row["consequence"]),
											', '.join(row["safeguard"]),
												row["propagated"],
												', '.join(row["risk"]),
												])
				counter += 1
	
	print(output.hazop_table)
	
	output.create_output()
	
	elapsed_time = time.time() - start_time
	print(elapsed_time)
	
	ontology_operations.save_ontology()

	# ===Get errors
	print(list(default_world.inconsistent_classes())) 