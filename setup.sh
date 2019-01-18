#note : you should run this script using sudo

cd ..
#Installing s2client-api
echo "Installing s2client-api"
git clone --recursive https://github.com/Blizzard/s2client-api && cd s2client-api
mkdir build && cd build
cmake ../
make -j 6
cd ..
# Install SC2 API headers
echo "Installing headers libraries"
sudo mkdir -p /opt/local/include
sudo cp -R include/sc2api /opt/local/include
sudo cp -R include/sc2renderer /opt/local/include
sudo cp -R include/sc2utils /opt/local/include
sudo cp -R build/generated/s2clientprotocol /opt/local/include
# Install protobuf headers
sudo cp -R contrib/protobuf/src/google /opt/local/include/sc2api
# Install SC2 API libraries
sudo mkdir -p /opt/local/lib/sc2api
sudo cp build/bin/libcivetweb.a /opt/local/lib/sc2api
sudo cp build/bin/libprotobuf.a /opt/local/lib/sc2api
sudo cp build/bin/libsc2api.a /opt/local/lib/sc2api
sudo cp build/bin/libsc2lib.a /opt/local/lib/sc2api
sudo cp build/bin/libsc2protocol.a /opt/local/lib/sc2api
sudo cp build/bin/libsc2utils.a /opt/local/lib/sc2api
cd ..
echo "Headers libraries' installation done"

#Redirecting to SC2 Data and Maps download page
echo "Download SC2 Data and Maps at the following page :
https://github.com/Blizzard/s2client-proto/blob/master/README.md#linux-packages"
mkdir StarCraftII
mkdir StarCraftII/Battle.net
mkdir StarCraftII/Maps
mkdir StarCraftII/Replays
mkdir StarCraftII/SC2Data
mkdir StarCraftII/Versions
sart "" https://github.com/Blizzard/s2client-proto/blob/master/README.md#linux-packages
cd ShyZergling/
