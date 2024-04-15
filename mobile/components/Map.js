import React, { useState } from "react";
import { View, Image } from "react-native";
import MapView, { Marker } from "react-native-maps";

import pin from "../assets/custom_pin.png";

export default function Map() {
  const [draggableCoord, setDraggableCoord] = useState({
    latitude: 39.541199,
    longitude: -119.806107,
  });

  return (
    <View className="h-full w-full">
      <MapView
        className="absolute bottom-0 left-0 right-0 top-0"
        initialRegion={{
          latitude: 39.541199,
          longitude: -119.806107,
          latitudeDelta: 0.042,
          longitudeDelta: 0.042,
        }}
      >
        <Marker
          draggable
          identifier="1"
          coordinate={draggableCoord}
          onDragEnd={(e) => e.nativeEvent.coordinate}
        >
          <Image source={pin} style={{ width: 40, height: 40 }} />
        </Marker>
      </MapView>
    </View>
  );
}
