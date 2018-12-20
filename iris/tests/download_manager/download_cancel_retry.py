# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'The download can be cancelled or retried.'
        self.test_case_id = '99470'
        self.test_suite_id = '1827'
        self.locales = ['en-US']

    def run(self):
        file_to_download = DownloadFiles.SMALL_FILE_20MB

        navigate('https://www.thinkbroadband.com/download')

        download_file(file_to_download, DownloadFiles.OK)

        expected = exists(DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL, 10)
        assert_true(self, expected, 'Cancel button is displayed.')

        click(DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL)
        expected = exists(DownloadManager.DownloadState.CANCELED, 10)
        assert_true(self, expected, 'Download was cancelled.')

        expected = exists(DownloadManager.DownloadsPanel.DOWNLOAD_RETRY, 10)
        assert_true(self, expected, 'Retry button is displayed.')

        click(DownloadManager.DownloadsPanel.DOWNLOAD_RETRY)
        expected = exists(DownloadManager.DownloadState.PROGRESS, 10)
        assert_true(self, expected, 'Download was restarted.')

    def teardown(self):
        click(DownloadManager.DownloadsPanel.DOWNLOAD_CANCEL)

        expected = exists(DownloadManager.DownloadState.CANCELED, 10)
        assert_true(self, expected, 'Download was cancelled.')
