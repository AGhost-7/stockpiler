const debug = process.env.NODE_ENV !== 'production'
const webpack = require('webpack')
const path = require('path')
const ExtractTextPlugin = require('extract-text-webpack-plugin')
const extractSass = new ExtractTextPlugin({
	filename: './public/css/[name].min.css',
	disable: process.env.NODE_ENV === 'development'
})

module.exports = {
	context: path.join(__dirname),
	devtool: debug ? 'inline-sourcemap' : null,
	entry: ['./src/js/index.js', './src/scss/index.scss'],
	devServer: { 
		inline: true, 
		port: 3000,
		publicPath: '/',
		contentBase: './public',
		hot: true,
		historyApiFallback: true
	},
	module: {
		loaders: [
			{
				test: /\.jsx?$/,
				exclude: /(node_modules|bower_components)/,
				loader: 'babel-loader',
				query: {
					presets: ['react', 'es2015', 'stage-0'],
					plugins: ['react-html-attrs', 'transform-class-properties', 'transform-decorators-legacy'],
				}
			},
			{
				test: /\.scss$/,
				loaders: ['style-loader', 'css-loader', 'sass-loader', 'sass']
			},
			{
				test: /\.css$/,
				loader: ['style-loader', 'css-loader']
			},
			{ 
				test: /\.(png|woff|woff2|eot|ttf|svg)$/,
				loader: 'url-loader?limit=100000'
			}
		],
		rules: [
			{
				test: /\.scss$/,
				use: [
					{
						loader: 'style-loader' // creates style nodes from JS strings
					}, 
					{
						loader: 'css-loader', // translates CSS into CommonJS
					},
					{
						loader: 'sass-loader', // compiles Sass to CSS
					}
				]
			}
		],
		resolve: {
			extensions: ['', '.js', '.jsx', '.css', '.scss'],
			modulesDirectories: ['node_modules']
		}
	},
	output: {
		path: path.join(__dirname, 'public'),
		filename: './js/index.js'
	},
	plugins: debug ? [] : [
		new webpack.optimize.DedupePlugin(),
		new webpack.optimize.OccurenceOrderPlugin(),
		new webpack.optimize.UglifyJsPlugin({ mangle: false, sourcemap: false }),
		extractSass
	],
}
