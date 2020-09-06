/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 * @flow strict-local
 */

import React from 'react';
import {
  SafeAreaView,
  StyleSheet,
  ScrollView,
  View,
  Text,
  Image,
  StatusBar,
  Alert,
} from 'react-native';

import { Button } from 'react-native-elements';
import Icon from 'react-native-vector-icons/FontAwesome';


const App: () => React$Node = () => {
  return (
    <>
      <StatusBar barStyle="dark-content" />
      <SafeAreaView>
        <View
          style={{
            padding: 20
          }}>
          <Image
            style={{width: 360}}
            source={require('./5.jpg')}
          />

        <Button
          title="Choice #1"
          style={styles.button}
          type='outline'
          onPress={() => Alert.alert('Simple Button pressed')}
          icon={
            <Icon
              name="check-circle"
              size={30}
            />
          }
          />

          <Button
          title="Choice #2"
          style={styles.button}
          type='outline'
          onPress={() => Alert.alert('Simple Button pressed')}
          icon={
            <Icon
              name="times-circle"
              size={30}
            />
          }
          />

        <Button
          title="Choice #3"
          style={styles.button}
          type='outline'
          onPress={() => Alert.alert('Simple Button pressed')}
          icon={
            <Icon
              name="times-circle"
              size={30}
            />
          }
          />

        <Button
          title="Choice #4"
          style={styles.button}
          type='outline'
          onPress={() => Alert.alert('Simple Button pressed')}
          icon={
            <Icon
              name="times-circle"
              size={30}
            />
          }
          />
        </View>
      </SafeAreaView>
    </>
  );
};

const styles = StyleSheet.create({
  button: {
    marginTop: 5,
    marginLeft: 10,
    marginRight: 10,
  }
});

export default App;
