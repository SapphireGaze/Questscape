import { View, Text, Pressable, Button } from "react-native";
import React, { useState } from 'react';
import Icon from "react-native-vector-icons/AntDesign";
import { launchCamera as _launchCamera, launchImageLibrary as _launchImageLibrary } from 'react-native-image-picker';
let launchCamera = _launchCamera;
let launchImageLibrary = _launchImageLibrary;



const PlayScreen = () => {

  const openImagePicker = () => {
    const options = {
      mediaType: 'photo',
      includeBase64: false,
      maxHeight: 2000,
      maxWidth: 2000,
    };

    launchImageLibrary(options, handleResponse);
  };

  const handleCameraLaunch = () => {
    const options = {
      mediaType: 'photo',
      includeBase64: false,
      maxHeight: 2000,
      maxWidth: 2000,
    }

    launchCamera(options, handleResponse);
  };

  const handleResponse = (response) => {
    if (response.didCancel) {
      console.log('User cancelled image picker');
    } else if (response.error) {
      console.log('Image picker error: ', response.error);
    } else {
      let imageUri = response.uri || response.assets?.[0]?.uri;
      setSelectedImage(imageUri);
    }
  };
  return (
    <View className="flex-1 bg-[#DEB887] p-12">
      <Pressable
        className="-ml-4 mt-6"
        onPress={() => navigation.navigate("Landing")}
      >
        <Text className="text-xl font-semibold text-gray-900">
          <Icon name="back" size={24} color="#111827" />
          &nbsp;Go Back
        </Text>
        <Pressable>
          <Button title="Open Camera" onPress={handleCameraLaunch} />
        </Pressable>
      </Pressable>
      <Text>Play</Text>
    </View>
  );
}
export default PlayScreen;