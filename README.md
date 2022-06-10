# Hattrick Sector Contribution Calculator

If you have a player in [hattrick](https://www.hattrick.org) and wish to 
train him for maximum impact (from skills, i.e. not special abilites), 
how should he be trained?

Set the `weeks` parameter in `main()` to the time available for 
training, and the script will provide the maximum impact the 
player can provide, depending on the position he is playing.

* The script does not implement a training simulator, estimated
  training times are taken from [Hattrick Portal](https://hattrickportal.pro/)
  Check script for more details.
* Maximum impact is calculated by adding up player contribution
  in all sectors. Different weights can be assigned to each combination 
  of player position/sector, to modify how the maximum impact is calculated.
