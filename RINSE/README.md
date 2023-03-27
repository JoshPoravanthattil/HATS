# Event-based Radiation-Induced-Noise Simulation Environment (Event-RINSE)
### by Seth Roffe

Fault injection framework for performing radiation-induced noise on neuromorphic sensor data. Preliminary data was collected at Los Alamos National Labs' under neutron radiation.

Non-internal python modules required:
 * numpy
 * scipy
 * cv2
 * moviepy

Data is assumed to have the format:
```
<X-Coordinate> <Y-Coordinate> <Timestamp> <Polarity>
```

Basic use:
```sh
python rinse.py -f <input_file> -o <output_file> --inject
```

Other argument flags:
 * -aoi <integer>: angle of incidence between radiation
 * -s <integer> <integer>: image size in pixels
 * -vi: view video of input file (Needs: cv2)
 * -vo: view video of output file (Needs: cv2)

For more information use:
```sh
python rinse.py -h
```

To install the dependencies
```sh
./install_dependencies.sh
```
