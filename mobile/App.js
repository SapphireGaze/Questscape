import { StatusBar } from 'expo-status-bar';
import { Button, StyleSheet, Text, View, Image, SafeAreaView } from 'react-native';
import Logo from './assets/hero.jpg';

export default function App() {
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.topContainer}>
        <Text style={styles.h1}>QuestScape</Text>
      </View>
      <View style={styles.middleContainer}>
        <Image
          source={Logo}
          style={styles.image}
        />
      </View>
      <View style={styles.buttonContainer}>
        <View style={styles.createButtonContainer}>
          <Button
            title="Create A Game"
            style={styles.createButtonContainer}
            onPress={() => this.onPress()}
            color="#fff"
          />
        </View>
        <View style={styles.joinButtonContainer}>
          <Button
            title="Join A Game"
            style={styles.joinButtonContainer}
            onPress={() => this.onPress()}
            color="#fff"
          />
        </View>
        <StatusBar style="auto" />
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#deb887',
    flex: 1,
    justifyContent: 'space-evenly',
  },
  topContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    margin: 20,
    padding: 10,
  },
  middleContainer: {
    flex: 3,
    justifyContent: 'flex-start',
    alignItems: 'center',
  },
  bottomContainer: {
    justifyContent: 'space-between',
    width: '90%',
    margin: 20,
    padding: 10,

  },
  h1: {
    color: '#87ADDE',
    fontSize: 48,
  },
  buttonContainer: {
    borderRadius: 10,
    padding: 8,
    margin: 8,
  },
  createButtonContainer: {
    marginTop: 'auto',
    backgroundColor: '#8b2861',
    borderRadius: 10,
    padding: 8,
    margin: 8,
  },
  joinButtonContainer: {
    marginTop: 'auto',
    backgroundColor: '#fe9a16',
    borderRadius: 10,
    padding: 8,
    margin: 8,
  },
  image: {
    width: 300,
    height: 260,
    justifyContent: 'center',
  }
});
