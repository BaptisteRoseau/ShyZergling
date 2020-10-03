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

#Installing s2client-proto
echo "Installing s2client-proto"
git clone --recursive https://github.com/Blizzard/s2client-proto && cd s2client-proto
echo "wget https://github.com/google/protobuf/releases/download/v3.4.0/protoc-3.4.0-linux-x86_64.zip \
unzip protoc-3.4.0-linux-x86_64.zip -d protoc3 && \
cp -r protoc3/bin/* /usr/bin/ && \
cp -r protoc3/include/* /usr/include/ && \
rm -rf protoc*" > install_protoc.sh
chmod 755 ./install_protoc.sh
sudo ./install_protoc.sh
sudo python setup.py build
sudo python setup.py install
cd ..

#Redirecting to SC2 Data and Maps download page
echo "Download SC2 Data and Maps at the following page :
https://github.com/Blizzard/s2client-proto/blob/master/README.md#linux-packages"
mkdir StarCraftII
mkdir StarCraftII/Battle.net
mkdir StarCraftII/Maps
mkdir StarCraftII/Replays
mkdir StarCraftII/SC2Data
mkdir StarCraftII/Versions

cd ShyZergling/
