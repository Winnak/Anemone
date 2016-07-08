/// <copyright file="BuildUtility.cs">
/// MIT License
///
/// Copyright(c) 2016 Erik Høyrup Jørgensen
///
/// Permission is hereby granted, free of charge, to any person obtaining a copy
/// of this software and associated documentation files (the "Software"), to deal
/// in the Software without restriction, including without limitation the rights
/// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
/// copies of the Software, and to permit persons to whom the Software is
/// furnished to do so, subject to the following conditions:
///
/// The above copyright notice and this permission notice shall be included in all
/// copies or substantial portions of the Software.
///
/// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
/// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
/// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
/// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
/// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
/// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
/// SOFTWARE.
/// </copyright>
/// <author>Erik Høyrup Jørgensen</author>
/// <date>03/25/2016 18:15</date>
/// <summary>Class for build methods required by Unity for the Anemone project.</summary>

/// <summary>
/// Part of the Anemone CI (https://github.com/winnak/anemone)
/// </summary>
namespace Anemone
{
    using System.Collections.Generic;
    using UnityEditor;
    using UnityEngine;

    /// <summary>
    /// Handles the internal methods of this library.
    /// </summary>
    internal static class BuildUtility
    {
        private const string kDefaultBuildPath = "./buildstmp/"; // has to be a unix file path
        private const string kDefaultBuildFile = "build.abc";

        /// <summary>
        /// Generalized build function, to be used by the different configurations.
        /// </summary>
        /// <param name="config">Build configuration found in the <see cref="kDefaultBuildFile"/>.</param>
        /// <param name="platform">Platform target.</param>
        /// <param name="options">Build options.</param>
        internal static void BuildProject(string config, BuildTarget platform, BuildOptions options)
        {
            if (BuildPipeline.isBuildingPlayer)
            {
                Debug.LogError("Anemone: BUILD FAILED! Unity is already building the project.");
                return;
            }

            ABCFormat configFile = ABCFormat.ParseFile(kDefaultBuildFile)[config];

            if (configFile == ABCFormat.NullNode)
            {
                Debug.LogError("Anemone: BUILD FAILED! Could not parse build configuration.");
                return;
            }


            Debug.Log("Anemone: Getting scenes.");
            string[] scenes = configFile.Get("scenes").Split(',');
            if ((scenes.Length == 1) && (scenes[0] == string.Empty))
            {
                scenes = GetScenes().ToArray();
            }
            else
            {
                for (int i = 0; i < scenes.Length; i++)
                {
                    Debug.Log("Anemone: " + scenes[i]);
                }
            }

            string buildFolder = configFile.Get("out");
            if (buildFolder == string.Empty)
            {
                Debug.LogWarning(string.Concat("Anemone: ",
                    "No output folder specified using ", kDefaultBuildPath,
                    " instead. Please set the \"out\" parameter in the project's ",
                    kDefaultBuildFile, " file."));

                buildFolder = kDefaultBuildPath;
            }

            Debug.Log("Anemone: Unity building.");
            string errorMessage = BuildPipeline.BuildPlayer(scenes, buildFolder, platform, options);

            if (!string.IsNullOrEmpty(errorMessage))
            {
                Debug.LogError("Anemone: " + errorMessage);
            }

            Debug.Log("Anemone: Finished.");
        }

        /// <summary>
        /// Fetches all scenes in the <see cref="EditorBuildSettings"/> and prints out which goes in and which does not.
        /// </summary>
        /// <returns>A list of active scenes.</returns>
        private static List<string> GetScenes()
        {
            List<string> levels = new List<string>();
            List<string> notadded = new List<string>();

            for (int i = 0; i < EditorBuildSettings.scenes.Length; i++)
            {
                string scenePath = EditorBuildSettings.scenes[i].path;
                if (EditorBuildSettings.scenes[i].enabled)
                {
                    levels.Add(scenePath);
                    Debug.Log(scenePath);
                }
                else
                {
                    notadded.Add(scenePath);
                }
            }

            if (notadded.Count > 0)
            {
                Debug.Log("Following scenes were not added:");
                for (int i = 0; i < notadded.Count; i++)
                {
                    Debug.Log(notadded[i]);
                }
            }

            return levels;
        }
    }
}
