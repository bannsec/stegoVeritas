
on: [push, pull_request]

name: Unit Tests
jobs:

  Linux:
    name: Linux Dockers
    runs-on: ubuntu-latest
    strategy:
        matrix:
            dockerfile: [Dockerfile.ubuntu.bionic, Dockerfile.ubuntu.focal, Dockerfile.debian, Dockerfile.fedora, Dockerfile.kali, Dockerfile.parrot]

    steps:
        -
            name: Set up Docker Buildx
            uses: docker/setup-buildx-action@v1
        -
            name: Build
            uses: docker/build-push-action@v2.6.1
            with:
                push: false
                file: Dockerfile.debian
                context: .


#    - name: Checkout
#      uses: actions/checkout@v2
#      with:
#          persist-credentials: false
#
#    - name: Install Conda
#      uses: goanpeca/setup-miniconda@v1
#      with:
#          auto-update-conda: true
#          python-version: 3.8
#
#    - name: Setup Conda
#      run: conda -h && conda create -n revenge python==3.8.2 && conda activate revenge && pip install requests
#
#    - name: Install radare2
#      run: conda activate revenge && python tests/windows/setup_windows_test_env.py
#    
#    - name: Add r2 to PATH
#      run: echo "::add-path::C:\Radare2\bin"
#
#    - name: Setup MSVC Environment
#      uses: ilammy/msvc-dev-cmd@v1.2.0
#
#    - name: Install angr
#      shell: cmd
#      run: conda activate revenge && git clone https://github.com/angr/angr-dev.git && cd angr-dev && git clone https://github.com/angr/vex.git && cd vex && nmake /f Makefile-msvc pub\libvex_guest_offsets.h && cd .. && setup.bat && pip install https://github.com/angr/angr-targets/archive/master.zip
#
#    - name: Install revenge
#      run: conda activate revenge && pip install .[dev]
#
#    - name: Run tests
#      shell: cmd
#      run: conda activate revenge && pytest -v tests/windows

