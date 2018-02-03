import React from 'react'

import Banner from '../components/banner'
import SignupForm from '../components/forms/signup'
import LoginForm from '../components/forms/login'

import BannerImg from 'file!../../images/banner_home.jpg'

import $ from 'jquery'

export default class HomePage extends React.Component {

	componentDidMount() {
		$('.tabs').tabs();
	}

	render() {
		return (
			<section id='home-page'>
				<Banner image={BannerImg} />
				<div class='container'>
					<div class='row'>
						<div class='col s12 m4 l4'>
							<h2>Cool point 1</h2>
							<p class='intro'>
								Lorem ipsum dolor sit amet, consectetur adipiscing elit.
								Nulla pretium condimentum ex, ultricies hendrerit quam.
							</p>
						</div>
						<div class='col s12 m4 l4'>
							<h2>Cool point 2</h2>
							<p class='intro'>
								Yellentesque est libero, fermentum ac magna id, ultrices luctus lectus.
								Curabitur ut enim non mi fermentum aliquam
							</p>
						</div>
						<div class='col s12 m4 l4'>
							<h2>Cool point 3</h2>
							<p class='intro'>
								Proin lacus magna, congue eu gravida in, condimentum quis nisl.
								Cras tempus erat purus, ac elementum erat vestibulum at.
							</p>
						</div>				
					</div>

					<div class="row">
						<div class="col s12">
							<ul class="tabs">
								<li class="tab col s3"><a href="#login">Login</a></li>
								<li class="tab col s3"><a href="#signup">Sign Up</a></li>
							</ul>
						</div>
						<div id="login" class="col s12">
							<p class="s12">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.</p>
							<LoginForm />
						</div>
						<div id="signup" class="col s12">
							<p class="s12">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.</p>
							<SignupForm />
						</div>
					</div>
				</div>
			</section>
			)
	}

}
