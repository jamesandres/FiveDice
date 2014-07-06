# Requirements

 * Ruby (tested with 1.9.3)
 * Gems: Sass, Compass
 * NPM 1.4.15 or greater
 * gulp js (npm install -g gulp)

# Install

    cd app
    npm install

# Building

    # Only if you want to clean everything out first
    ./node_modules/gulp/bin/gulp.js clean
    ./node_modules/gulp/bin/gulp.js watch

# Testing

    ./node_modules/karma/bin/karma start karma.conf.js
