module.exports = {
    "transpileDependencies": [
        "vuetify"
    ],
    publicPath: '/',
    devServer: {
        port: 8001,
        proxy: 'http://localhost:8000'
    }
}