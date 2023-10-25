# from parchmint.device import Device
# import sys
# import json
# # file_path = sys.argv[1]

# file_path = "../Microfluidics-Benchmarks/3DuF_Design/test2.json"
# file_path_out = "../Microfluidics-Benchmarks/3DuF_Design/test2_clean.json"

# print("File Name: " + file_path)
# device = None
# with open(file_path) as data_file:
#     json_data = json.load(data_file)
#     device = Device.from_parchmint_v1_2(json_data)
# print("Checking for components with no dimensions:")
# # print(device)
# for component in device.components:
#     print(component)
#     if component.xspan != -1 or component.yspan != -1:
#         print(
#             "Component - {} | Type - {} | Dimensions - ({}, {})".format(
#                 component.ID, component.entity, component.xspan, component.yspan
#             )
#         )


#     if 'rotation' in component and component.rotation != 0:
#         print("initiate rotate degree")
#         component.rotation = 0

#     for port in component.ports:
#         if port.x != -1 or port.y != -1:
#             print("Component - {} | Type - {} | Port {} - ({}, {})".format(
#                 component.ID, component.entity, port.label, port.x, port.y
#             ))


# print("Checking for components with no ports:")
# for component in device.components:
#     if len(component.ports) == 0:
#         print("Component - {} | Type - {}".format(component.ID, component.entity))

# with open(file_path_out, "w") as out_file:
#     json.dump(json_data, out_file)