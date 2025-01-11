# FileMover

The purpose of this program is to move files from one location into the current milling folder.

A shade guide dictionary is included to convert shades to Vita.

There are 3 options for source/destination:
    Milling folder
        Source - Y:\ManufacturingDir\<date>\NDX Standard FCZ
        Destination - Y:\ManufacturingDir\<date>\NDX Standard FCZ
    New CAM files - NDX Standard FCZ
        Source - Y:\ManufacturingDir\New CAM Files\NDX Standard FCZ
        Destination - Y:\ManufacturingDir\<date>\NDX Standard FCZ
    Other
        Source/destination are both user-defined.

It is intended to set the source/destination at the start of the day, then leave the program running throughout the day to stay efficient.

Scan or enter case numbers which will be added to a list. The shades will be extracted via regex as long as the file name is formatted as follows:
    CASE#_TYPE_PAN_TOOTH#_SHADE_REMAININGTEXT.EXTENSION

Example file:
    11824359_FCZ_2001_19_1M2_JOHN.D_MIWYO_NDXSTONE.STL

Folders will be created based off the shades extracted and the files will be moved into them.

A table will display the cases scanned as well as the shade and file name. It will also display any scanned cases that were not found in the source folder.