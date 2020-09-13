import React, {Component} from 'react';
import _, { shuffle, random } from 'underscore';
import {
  Alert,
  Image,
  View,
  StyleSheet
} from 'react-native';
import {
  Header,
  Button,
} from 'react-native-elements';
import Icon from 'react-native-vector-icons/FontAwesome';

import storage from '@react-native-firebase/storage';
import firestore from '@react-native-firebase/firestore';


class Guess extends Component {
  state = {
    level: 0,
    errors: 0,
    stars: [],
    image: null,
    options: [],
    answer: '',
    buttons: [],
  };

  returnLevel = () => {
    return `${this.state.level}/${this.state.stars.length}`
  }

  returnErrors() {
    return `${this.state.errors}`
  }

  generateOptions(star) {
    const totalOptions = 4;
    const similarStars = this.state.stars.filter(e =>
      e.category === star.category && e.name !== star.name
    );
    var options = shuffle(similarStars)
      .slice(0, totalOptions)
      .map(e => e.name);
    options.splice(random(0, totalOptions-1), 1, star.name);
    return options;
  }

  async loadStars() {
    let stars = [];
    const starsData = await firestore()
      .collection('stars')
      .get();
    starsData.forEach((elem) => {
      stars.push(elem.data());
    });
    this.setState({
      stars: shuffle(stars)
    });
  }

  checkOption(event, optionSelected) {
    // Alert.alert('Calling my function')
    this.setState((state) => {
      let newButtons = [];
      let errors = state.errors;
      state.buttons.forEach((button) => {
        if(button.props.title === optionSelected) {
          let icon = 'check-circle';
          if(optionSelected !== state.answer) {
            icon = 'times-circle';
            errors++;
          }
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
      state.errors = errors;
      state.buttons = newButtons;
      return state;
    });
    // Add transition animation
    setTimeout(() => {this.nextLevel()}, 800)
  };

  async loadLevel(levelIndex) {
    const star = this.state.stars[levelIndex];
    const options = this.generateOptions(star);
    const answer = star.name;
    const imageRef = storage().ref(`/images/${star.starId}.jpg`);
    const image = await imageRef.getDownloadURL();
    // console.log('This is image', image);
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
    // Rerender parent as we want to access updated child data via ref
    this.props.rerender();
  }

  nextLevel() {
    const newLevel = this.state.level + 1;
    const totalLevels = this.state.stars.length;
    if(newLevel >= totalLevels) {
      Alert.alert('End of the game');
      return
    }

    this.setState({
      level: newLevel
    });
    this.loadLevel(newLevel);
  }

  async componentDidMount() {
    await this.loadStars();
    await this.loadLevel(this.state.level);
  }

  render(props) {
    const current = this.state.level+1;
    const total = this.state.stars.length;
    return (
      <View style={styles.mainView}>
        <View style={styles.imageContainer}>
          <Image
            style={[{width: 240, height: 360}, styles.image]}
            source={{uri: this.state.image}}
          />
        </View>
        {this.state.buttons}
      </View>
    );
  }
}

const styles = StyleSheet.create({
  mainView: {
    // padding: 20,
  },
  button: {
    marginTop: 3,
    marginLeft: 10,
    marginRight: 10,
  },
  imageContainer: {
    marginTop: 10,
    marginBottom: 10,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  image: {
    borderRadius: 15,
  }
});

export default Guess;
