// Drink list: beer, whiteWine, redWine, water, coke

window.entityProfiles = {

  beerLots: {
    name: 'beerLots',
    drink: { // % chance of drink, total equals 100
      beer: 100
    },
    actionPropensity: { // % chance of event, total equals 100
      bar: 70,
      toilet: 30,
      smoke: 0
    },
    waiting: { // waiting time for event in seconds
      bar: 180,
      toilet: 210,
      smoke: 240
    }
  },
  beerToilet: {
    name: 'beerToilet',
    drink: {
      beer: 100
    },
    actionPropensity: {
      bar: 30,
      toilet: 50,
      smoke: 20
    },
    waiting: {
      bar: 180,
      toilet: 210,
      smoke: 240
    }
  },
  beerSmoke: {
    name: 'beerSmoke',
    drink: {
      beer: 100
    },
    actionPropensity: {
      bar: 50,
      toilet: 20,
      smoke: 30
    },
    waiting: {
      bar: 180,
      toilet: 210,
      smoke: 240
    }
  },
  whiteWineLots: {
    name: 'whiteWineLots',
    drink: {
      whiteWine: 100
    },
    actionPropensity: {
      bar: 50,
      toilet: 50,
      smoke: 0
    },
    waiting: {
      bar: 180,
      toilet: 210,
      smoke: 240
    }
  },
  whiteWineToilet: {
    name: 'whiteWineToilet',
    drink: {
      whiteWine: 100
    },
    actionPropensity: {
      bar: 30,
      toilet: 60,
      smoke: 10
    },
    waiting: {
      bar: 180,
      toilet: 210,
      smoke: 240
    }
  },
  mixedWine: {
    name: 'mixedWine',
    drink: {
      whiteWine: 70,
      redWine: 30
    },
    actionPropensity: {
      bar: 50,
      toilet: 30,
      smoke: 20
    },
    waiting: {
      bar: 180,
      toilet: 210,
      smoke: 240
    }
  },
  redWine: {
    name: 'redWine',
    drink: {
      redWine: 100
    },
    actionPropensity: {
      bar: 30,
      toilet: 40,
      smoke: 30
    },
    waiting: {
      bar: 180,
      toilet: 210,
      smoke: 240
    }
  },
  waterMostly: {
    name: 'waterMostly',
    drink: {
      water: 80,
      coke: 20
    },
    actionPropensity: {
      bar: 40,
      toilet: 40,
      smoke: 20
    },
    waiting: {
      bar: 180,
      toilet: 210,
      smoke: 240
    }
  },
  cokeMostly: {
    name: 'cokeMostly',
    drink: {
      coke: 80,
      water: 20
    },
    actionPropensity: {
      bar: 60,
      toilet: 40,
      smoke: 0
    },
    waiting: {
      bar: 180,
      toilet: 210,
      smoke: 240
    }
  }
}

window.selectProfile = function (random) {
  if (random < 0.1) {
    return window.entityProfiles.beerLots
  } else if (random < 0.2) {
    return window.entityProfiles.beerLots
  } else if (random < 0.3) {
    return window.entityProfiles.beerToilet
  } else if (random < 0.4) {
    return window.entityProfiles.beerSmoke
  } else if (random < 0.5) {
    return window.entityProfiles.whiteWineLots
  } else if (random < 0.6) {
    return window.entityProfiles.whiteWineToilet
  } else if (random < 0.7) {
    return window.entityProfiles.mixedWine
  } else if (random < 0.8) {
    return window.entityProfiles.redWine
  } else if (random < 0.9) {
    return window.entityProfiles.waterMostly
  } else if (random < 1) {
    return window.entityProfiles.cokeMostly
  }
}
