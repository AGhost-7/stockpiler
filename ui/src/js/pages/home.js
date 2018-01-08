import React from 'react'


export default class HomePage extends React.Component {
	

	componentDidMount() {
		
	}

	render() {
		return (
			<section id='home-page'>
				<div id='banner' class='row'>
					<img class='img' src='http://fakeimg.pl/1200x500/' />
				</div>
				<div class='container'>
					<div class='row'>
						<div class='col s12 m4 l4'>
							<h2>Cool point 1</h2>
							<p class='intro'>
							Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla pretium condimentum ex, ultricies hendrerit quam.
							</p>
						</div>
						<div class='col s12 m4 l4'>
							<h2>Cool point 2</h2>
							<p class='intro'>
							Yellentesque est libero, fermentum ac magna id, ultrices luctus lectus. Curabitur ut enim non mi fermentum aliquam
							</p>
						</div>
						<div class='col s12 m4 l4'>
							<h2>Cool point 3</h2>
							<p class='intro'>
							Proin lacus magna, congue eu gravida in, condimentum quis nisl. Cras tempus erat purus, ac elementum erat vestibulum at.
							</p>
						</div>				
					</div>
					<div class='row'>
						<div class='col s12 center-align'>
							<button class='waves-effect waves-light btn'>Get Started</button>
						</div>
					</div>
				</div>
			</section>
		)
	}

}

