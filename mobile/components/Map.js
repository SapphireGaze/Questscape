import React, { Component } from "react";
import { Dimensions, View, Image } from "react-native";
import MapView, { Marker } from "react-native-maps";

import pin from "../assets/custom_pin.png";

const { height, width } = Dimensions.get("window");

export default class Map extends Component {
  render() {
    return (
      <View style={{ height: height, width: width }}>
        <MapView
          style={{ position: "absolute", left: 0, top: 0, right: 0, bottom: 0 }}
          initialRegion={{
            latitude: 39.541199,
            longitude: -119.806107,
            latitudeDelta: 0.042,
            longitudeDelta: 0.042,
          }}
        >
          <Marker coordinate={{ latitude: 39.541199, longitude: -119.806107 }}>
            <Image source={pin} style={{ width: 30, height: 30 }} />
          </Marker>
        </MapView>
      </View>
    );
  }
}
