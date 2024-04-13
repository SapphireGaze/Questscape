import * as React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

import LandingScreen from "./screens/LandingScreen";

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        screenOptions={{
          animation: "none",
          headerShown: false,
        }}
      >
        <Stack.Screen name="Landing" component={LandingScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
