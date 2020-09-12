/**
 *
 * @format
 * @flow strict-local
 */

import React, {Component, useState} from 'react';
import {
  SafeAreaView,
  StyleSheet,
  View,
  Text,
  Image,
  StatusBar,
  Alert,
} from 'react-native';
import {
  ListItem,
} from 'react-native-elements';
import Animated from 'react-native-reanimated';
import RBSheet from "react-native-raw-bottom-sheet";
import BottomSheet from 'reanimated-bottom-sheet';
import Guess from './components/Guess';


const App = () => {
  const [isVisible, setIsVisible] = useState(true);
  const list = [
    { title: 'List Item 1' },
    { title: 'List Item 2' },
    {
      title: 'Cancel',
      containerStyle: { backgroundColor: 'red' },
      titleStyle: { color: 'white' },
      onPress: () => setIsVisible(false),
    },
  ];
  const renderContent = () => (
    <View
      style={{
        backgroundColor: 'papayawhip',
        padding: 16,
        height: 400,
      }}
    >
      <Text>Swipe down to close</Text>
    </View>
  );
  const sheetRef = React.useRef(null);
  const refRBSheet = React.useRef();
  return (
    <>
      <StatusBar barStyle="dark-content" />
      <SafeAreaView>
        <View
          style={{
            padding: 20
          }}>
          <Guess />
        </View>
        <RBSheet
        ref={refRBSheet}
        closeOnDragDown={true}
        closeOnPressMask={false}
        customStyles={{
          wrapper: {
            backgroundColor: "transparent"
          },
          draggableIcon: {
            backgroundColor: "#000"
          }
        }}
      />
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
