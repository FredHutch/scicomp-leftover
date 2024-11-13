release=${RELEASE}
package=${PACKAGE}

rootdir=debian/$(package)_$(release)
pkgdir=$(rootdir)/DEBIAN
libdir=$(rootdir)/usr/local/lib
sbindir=$(rootdir)/usr/local/sbin

all:
	echo "No \"all\" target actions set ATM"

buildenv:
	python3 -m venv ~/venv
	. ~/venv/bin/activate && \
		python3 -m pip install --upgrade pyinstaller

build: buildenv
	. ~/venv/bin/activate && \
		pyinstaller src/scicomp-leftover/leftover.py --name leftover

$(rootdir):
	mkdir -p $(rootdir)

$(libdir): $(rootdir)
	mkdir -p $(libdir)

$(sbindir): $(rootdir)
	mkdir -p $(sbindir)

$(pkgdir): $(rootdir)
	mkdir -p $(pkgdir)

control $(pkgdir)/control: $(pkgdir)
	cat debian/control | envsubst > $(pkgdir)/control

postinst $(pkgdir)/postinst: $(pkgdir)
	cp debian/postinst $(pkgdir)/postinst
	chmod 0755 $(pkgdir)/postinst

prerm $(pkgdir)/prerm: $(pkgdir)
	cp debian/prerm $(pkgdir)/prerm
	chmod 0755 $(pkgdir)/prerm

pkgcontrol: control postinst prerm

install: build pkgcontrol $(libdir) $(sbindir)
	cp -r dist/leftover $(libdir)

deb: install
	dpkg-deb --build $(rootdir)

clean:
	rm -r build \
		debian/scicomp-leftover_* \
		dist \
		leftover.spec \
		scicomp-leftover.spec
