import { UniqueFieldDefinitionNamesRule } from 'graphql';
/**
 *
 * @format
 * @flow strict-local
 */

import React, {Component, useState, useEffect} from 'react';
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
  Header,
  ListItem,
  BottomSheet,
} from 'react-native-elements';
import Animated from 'react-native-reanimated';
import Guess from './components/Guess';


class App extends Component {
  state = {
    isVisible: false
  }

  constructor(props) {
    super();
    this.guessRef = React.createRef();
    this.rerenderParentCallback = this.rerenderParentCallback.bind(this);
  }

  rerenderParentCallback() {
    this.forceUpdate();
  }

  render(props) {
    const list = [
      { title: 'New game' },
      { title: 'Leaderboard' },
      {
        title: 'Cancel',
        containerStyle: { backgroundColor: 'red' },
        titleStyle: { color: 'white' },
        onPress: () => this.setState({isVisible: false}),
      },
    ];
    let currentLevel = '';
    let currentErrors = '';
    if(this.guessRef.current !== null) {
      currentLevel = this.guessRef.current.returnLevel();
      currentErrors = this.guessRef.current.returnErrors();
    }

    return (
      <>
        <StatusBar backgroundColor="green" barStyle="dark-content" />
        <SafeAreaView>
          <Header
            leftComponent={{ icon: 'menu', color: '#fff', onPress: () => this.setState({isVisible: true}) }}
            centerComponent={{ text: `${currentLevel}`, style: { color: '#fff' } }}
            rightComponent={{ text: `${currentErrors}`, style: {color: '#fff' } }}
          />
          <Guess ref={this.guessRef} rerender={this.rerenderParentCallback}/>
          <BottomSheet isVisible={this.state.isVisible}>
            {list.map((l, i) => (
              <ListItem key={i} containerStyle={l.containerStyle} onPress={l.onPress}>
                <ListItem.Content>
                  <ListItem.Title style={l.titleStyle}>{l.title}</ListItem.Title>
                </ListItem.Content>
              </ListItem>
            ))}
          </BottomSheet>
        </SafeAreaView>
      </>
    );
  }
};

const styles = StyleSheet.create({
  button: {
    marginTop: 5,
    marginLeft: 10,
    marginRight: 10,
  },
  containerStyle: {

  }
});

export default App;
