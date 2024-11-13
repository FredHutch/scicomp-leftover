release=${RELEASE}
all:
	echo "No \"all\" target actions set ATM"



deb:
	mkdir -p debian/scicomp-leftover_$(release) \
		debian/scicomp-leftover_$(release)/usr \
		debian/scicomp-leftover_$(release)/usr/local \
		debian/scicomp-leftover_$(release)/usr/local/lib \
		debian/scicomp-leftover_$(release)/usr/local/bin \
		debian/scicomp-leftover_$(release)/DEBIAN
	cat debian/control | envsubst > \
		debian/scicomp-leftover_$(release)/DEBIAN/control

clean:
	rm -r build \
		debian/scicomp-leftover_* \
		dist \
		leftover.spec \
		scicomp-leftover.spec
