release=${RELEASE}
all:
	echo "No \"all\" target actions set ATM"

buildenv:
	python3 -m venv ~/venv
	. ~/venv/bin/activate && \
		python3 -m pip install --upgrade pyinstaller

build: buildenv
	. ~/venv/bin/activate && \
		pyinstaller src/scicomp-leftover/leftover.py --name leftover

debdirs:
	mkdir -p debian/scicomp-leftover_$(release) \
		debian/scicomp-leftover_$(release)/usr \
		debian/scicomp-leftover_$(release)/usr/local \
		debian/scicomp-leftover_$(release)/usr/local/lib \
		debian/scicomp-leftover_$(release)/usr/local/sbin \
		debian/scicomp-leftover_$(release)/DEBIAN

control: debdirs
	cat debian/control | envsubst > \
		debian/scicomp-leftover_$(release)/DEBIAN/control
	cp debian/postinst debian/scicomp-leftover_$(release)/DEBIAN/postinst
	cp debian/prerm debian/scicomp-leftover_$(release)/DEBIAN/prerm

install: build debdirs
	cp -r dist/leftover debian/scicomp-leftover_$(release)/usr/local/lib/


clean:
	rm -r build \
		debian/scicomp-leftover_* \
		dist \
		leftover.spec \
		scicomp-leftover.spec
