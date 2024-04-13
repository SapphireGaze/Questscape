import { View, Pressable, Text } from "react-native";

import Icon from "react-native-vector-icons/AntDesign";

export default function CreateScreen({ navigation }) {
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
      </Pressable>
      <Text>Create</Text>
    </View>
  );
}
