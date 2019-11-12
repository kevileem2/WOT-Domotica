window.onload = () => {
  let db = firebase.firestore()
  var configRef = db.collection('smartHomeConfig').doc('config1')
  var sensorRef = db.collection('smartHomeConfig').doc('sensors')

  // Valid options for source are 'server', 'cache', or
  // 'default'. See https://firebase.google.com/docs/reference/js/firebase.firestore.GetOptions
  // for more information.
  var getOptions = {
    source: 'server',
  }

  let configKeys = {}

  const eventListener = () => {
    const allCheckboxes = document.getElementsByClassName('form-check-input')
    for (let i = 0; i < allCheckboxes.length; i++) {
      const checkbox = allCheckboxes[i]
      checkbox.addEventListener('change', () => {
        const id = checkbox.id
        const isChecked = checkbox.checked
        configKeys[id] = isChecked
        configRef.set(configKeys)
      })
    }
  }

  sensorRef.get(getOptions).then(doc => {
    console.log(doc.data())
    for (key in doc.data()) {
      if (doc.data().hasOwnProperty(key)) {
        const makeContainerEl = document.createElement('div')
        makeContainerEl.className = 'col-4 offset-4'
        const makeP = document.createElement('p')
        makeP.innerHTML = `${key}: ${doc.data()[key]}`
        makeContainerEl.appendChild(makeP)
        const appDataEl = document.getElementById('appSensors')
        appDataEl.appendChild(makeContainerEl)
      }
    }
  })

  configRef
    .get(getOptions)
    .then(doc => {
      for (key in doc.data()) {
        if (doc.data().hasOwnProperty(key)) {
          const makeContainerEl = document.createElement('div')
          makeContainerEl.className =
            'form-check form-check-inline col-4 offset-4'
          const makeCheckBox = document.createElement('input')
          makeCheckBox.className = 'form-check-input'
          makeCheckBox.type = 'checkbox'
          makeCheckBox.id = `${key}`
          makeCheckBox.checked = doc.data()[key]
          const makeLabel = document.createElement('label')
          makeLabel.className = 'form-check-label'
          makeLabel.for = `${doc.data()[key]}`
          makeLabel.innerHTML = `${key}`
          makeContainerEl.appendChild(makeCheckBox)
          makeContainerEl.appendChild(makeLabel)
          const appDataEl = document.getElementById('appData')
          appDataEl.appendChild(makeContainerEl)
          configKeys[key] = doc.data()[key]
        }
      }
      eventListener()
    })
    .catch(error => {
      console.log('Error getting document:', error)
    })
}
