## TODO
* json file mit Haltestellen erweitern, eventuell type hinzufügen (stop, poi etc)
* Command Dissemination
  * line 110, json file Verarbeitung ggf. anpassen
  * wenn so etwas "Fahre zur nächst gelegenden Haltestelle" drin sein soll, muss die Node vermutlich zu adore_ros2_msgs/msg/VehicleStateDynamic subscirben, damit man dann die nächste Haltestelle berechnen kann
  * resolve_named_goal (liuen 139) müsste angepasst werden, sodass Haltestellen und so etwas wie "nächste" etc erkannt wird, eventuell kann man das aber auch aufspliten und einen command haben, der zu einer spezifischen Haltestelle fährt und einen, der zur nächsten fährt. Dann sollte das auch über das LLM Model erkannt werden können.
  * nearest distance Berechnung muss dannn noch hinzugefügt werden
  * um den Command dann final zu verarbeiten muss eigentlich nur einer neuer Goal Point gesetzt werden (siehe Commmand Verabeitung von GOTO/ DRIVE TO)