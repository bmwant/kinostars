/**
 *
 * @format
 * @flow strict-local
 */

import React, {Component} from 'react';
import {
  SafeAreaView,
  StyleSheet,
  View,
  Text,
  Image,
  StatusBar,
  Alert,
} from 'react-native';

import { Button } from 'react-native-elements';
import Icon from 'react-native-vector-icons/FontAwesome';

const levels = [{
  options: ['Some name', 'Name Surname', 'Another name', 'Last name'],
  answer: 'Name Surname',
  image: require('./5.jpg'),
},
{
  options: ['Some name 2', 'Name Surname 2', 'Another name 2', 'Last name 2'],
  answer: 'Name Surname 2',
  image: require('./58.jpg'),
}];

class Guess extends Component {
  state = {
    level: 0,
    image: null,
    options: [],
    answer: '',
    buttons: [],
  };

  checkOption(event, optionSelected) {
    // Alert.alert('Calling my function')
    this.setState((state) => {
      let newButtons = [];
      state.buttons.forEach((button) => {
        if(button.props.title === optionSelected) {
          const icon = optionSelected === state.answer ? 'check-circle' : 'times-circle';
          const selectedButton = (<Button
            title={optionSelected}
            key={optionSelected}
            type='outline'
            style={styles.button}
            icon={
              <Icon
                name={icon}
                size={30}
              />
            }
          />);
          newButtons.push(selectedButton);
        } else {
          const disabledButton = (<Button
            title={button.props.title}
            key={button.props.title}
            type='outline'
            style={styles.button}
            disabled
          />);
          newButtons.push(disabledButton);
        }
      });
      state.buttons = newButtons;
      return state;
    });
    // Add transition animation
    setTimeout(() => {this.nextLevel()}, 1000)
  };

  loadStar(levelIndex) {
    const options = levels[levelIndex].options;
    const answer = levels[levelIndex].answer;
    const image = levels[levelIndex].image;
    buttons = options.map(choice => (
      <Button
        title={choice}
        key={choice}
        type='outline'
        onPress={(event) => this.checkOption(event, choice)}
        style={styles.button}
      />)
    );
    this.setState({
      image: image,
      answer: answer,
      buttons: buttons
    });

  }

  nextLevel() {
    const newLevel = this.state.level + 1;
    if(newLevel >= levels.length) {
      Alert.alert('End of the game');
      return
    }

    this.setState({
      level: newLevel
    });
    this.loadStar(newLevel);
  }

  componentDidMount() {
    this.loadStar(this.state.level);
  }

  render(props) {
    return (
      <>
        <Image
          style={{width: 360}}
          source={this.state.image}
        />
        {this.state.buttons}
      </>
    );
  }
}

const App = () => {
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
      </SafeAreaView>
    </>
  );
};

const styles = StyleSheet.create({
  button: {
    marginTop: 5,
    marginLeft: 10,
    marginRight: 10,
  },
  buttonRight: {
    backgroundColor: 'green'
  },
  buttonWrong: {

  }
});

export default App;
