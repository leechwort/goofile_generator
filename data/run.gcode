;Template for chitubox zip file generation
;fileName:
;machineType:Unknown
;estimatedPrintTime:336
;volume:0.124
;resin:
;weight:0
;price:0
;layerHeight:0.1
;resolutionX:11520
;resolutionY:5120
;machineX:218.88
;machineY:122.88
;machineZ:10
;projectType:Normal
;normalExposureTime:15
;bottomLayExposureTime:30
;bottomLayerExposureTime:30
;normalDropSpeed:500
;normalLayerLiftSpeed:100
;normalLayerLiftHeight:5
;zSlowUpDistance:0
;bottomLayCount:4
;bottomLayerCount:4
;mirror:0
;totalLayer:1
;bottomLayerLiftHeight:1
;bottomLayerLiftSpeed:500
;bottomLightOffTime:0
;lightOffTime:0
;bottomPWMLight:255
;PWMLight:255
;antiAliasLevel:1

;START_GCODE_BEGIN
;G21;Set units to be mm
;G90;Absolute positioning
;M17;Enable motors
;M106 S0;Turn LED OFF
;<Slice> Blank
;G28 Z0;Home Z
;END_GCODE_BEGIN

;LAYER_START:0
;PositionZ:0.1mm
M6054 "1.png";Show image
;G0 Z5.1 F100;Z Lift (1)
;G0 Z0.1 F100;Retract (1)
;G4 P0;Wait before cure
M106 S255;Turn LED ON
G4 P50000;Cure time/delay
M106 S0;Turn LED OFF
;<Slice> Blank
;LAYER_END

;START_GCODE_END
;M106 S0;Turn LED OFF
;G0 Z5.1 F100;Z Lift (1)
;G1 Z0 F500;Move Z
;M18;Disable motors
;END_GCODE_END
;<Completed>
